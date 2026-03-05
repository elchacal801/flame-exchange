/**
 * viz.js - FLAME Visualization Suite
 *
 * Three visualization components for fraud intelligence:
 * 1. Enhanced Global Relationship Graph (D3 force-directed)
 * 2. Per-TP Ego Neighborhood Graph (D3 force-directed)
 * 3. CFPF Attack Flow Diagram (HTML/CSS)
 */

const FlameViz = (function () {
    'use strict';

    // -------------------------------------------------------------------
    // Shared Constants
    // -------------------------------------------------------------------

    const REL_COLORS = {
        'feeds-into': '#ef4444',
        'enables': '#3b82f6',
        'enhances': '#a855f7',
        'provides-mules-for': '#22c55e',
        'shares-infrastructure': '#f97316',
        'escalates-from': '#eab308',
        'related-to': '#6b7280',
    };

    const REL_LABELS = {
        'feeds-into': 'Feeds Into',
        'enables': 'Enables',
        'enhances': 'Enhances',
        'provides-mules-for': 'Provides Mules',
        'shares-infrastructure': 'Shares Infra',
        'escalates-from': 'Escalates From',
        'related-to': 'Related To',
    };

    const REL_REVERSE = {
        'feeds-into': 'fed-by',
        'enables': 'enabled-by',
        'enhances': 'enhanced-by',
        'provides-mules-for': 'receives-mules-from',
        'shares-infrastructure': 'shares-infrastructure',
        'escalates-from': 'escalates-to',
        'related-to': 'related-to',
    };

    const SECTOR_COLORS = [
        '#0ea5e9', '#f43f5e', '#a78bfa', '#34d399', '#fbbf24',
        '#06b6d4', '#fb923c', '#e879f9', '#4ade80', '#f87171'
    ];

    const PHASE_INFO = {
        P1: { label: 'P1', name: 'Recon', color: '#f97316' },
        P2: { label: 'P2', name: 'Initial Access', color: '#ef4444' },
        P3: { label: 'P3', name: 'Positioning', color: '#a855f7' },
        P4: { label: 'P4', name: 'Execution', color: '#3b82f6' },
        P5: { label: 'P5', name: 'Monetization', color: '#22c55e' },
    };

    const PHASE_ORDER = ['P1', 'P2', 'P3', 'P4', 'P5'];

    // -------------------------------------------------------------------
    // Shared State
    // -------------------------------------------------------------------

    let _reverseRelIndex = null;
    let _sectorColorMap = {};
    let _data = null;

    // -------------------------------------------------------------------
    // Shared Utilities
    // -------------------------------------------------------------------

    function buildReverseRelationshipIndex(data) {
        _data = data;
        _reverseRelIndex = {};

        // Build sector color map
        var sectorSet = {};
        data.forEach(function (tp) {
            var s = (tp.sectors && tp.sectors[0]) || 'other';
            sectorSet[s] = true;
        });
        Object.keys(sectorSet).sort().forEach(function (s, i) {
            _sectorColorMap[s] = SECTOR_COLORS[i % SECTOR_COLORS.length];
        });

        // Build reverse index
        data.forEach(function (tp) {
            if (!_reverseRelIndex[tp.id]) _reverseRelIndex[tp.id] = [];
            (tp.related_tps || []).forEach(function (rel) {
                if (!_reverseRelIndex[rel.id]) _reverseRelIndex[rel.id] = [];
                // Check if reverse already exists in raw data (avoid synthetic duplicate)
                var targetTP = data.find(function (t) { return t.id === rel.id; });
                var alreadyBidirectional = targetTP && (targetTP.related_tps || []).some(function (r) {
                    return r.id === tp.id;
                });
                if (!alreadyBidirectional) {
                    _reverseRelIndex[rel.id].push({
                        id: tp.id,
                        relationship: REL_REVERSE[rel.relationship] || rel.relationship,
                        direction: 'inbound'
                    });
                }
            });
        });
    }

    function exportSVG(svgElement, filename) {
        var serializer = new XMLSerializer();
        var svgString = serializer.serializeToString(svgElement);
        var blob = new Blob([svgString], { type: 'image/svg+xml' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename || 'flame-graph.svg';
        a.click();
        URL.revokeObjectURL(url);
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str || ''));
        return div.innerHTML;
    }

    function formatLabel(s) {
        return (s || '').replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    }

    // -------------------------------------------------------------------
    // Component 3: CFPF Attack Flow Diagram
    // -------------------------------------------------------------------

    function extractPhaseMapping(bodyMarkdown) {
        var phases = {};
        var phaseRegex = /### Phase (\d): ([^\n]+)\n([\s\S]*?)(?=\n### Phase |\n## |\n---\s*$|$)/g;
        var match;
        while ((match = phaseRegex.exec(bodyMarkdown)) !== null) {
            var phaseKey = 'P' + match[1];
            var phaseName = match[2].trim();
            var sectionBody = match[3];
            var techniques = [];
            var rowRegex = /\| ([^|]+)\| ([^|]+)\|/g;
            var rowMatch;
            while ((rowMatch = rowRegex.exec(sectionBody)) !== null) {
                var col1 = rowMatch[1].trim();
                if (col1 === 'Technique' || col1.startsWith('---') || col1 === '') continue;
                var parts = col1.split(': ');
                var techName = parts.length > 1 ? parts.slice(1).join(': ') : col1;
                techniques.push({ id: parts[0] || '', name: techName });
            }
            if (techniques.length > 0) {
                phases[phaseKey] = { name: phaseName, techniques: techniques };
            }
        }
        return phases;
    }

    function renderAttackFlow(container, tpItem, detectionRules) {
        if (!container || !tpItem || !tpItem.body) return;

        var phaseMapping = extractPhaseMapping(tpItem.body);
        var activePhases = tpItem.cfpf_phases || [];

        // Map detection rules to phases
        var rulesByPhase = {};
        if (detectionRules && detectionRules.length > 0) {
            detectionRules.forEach(function (rule) {
                var phase = rule.cfpf_phase;
                if (phase) {
                    if (!rulesByPhase[phase]) rulesByPhase[phase] = [];
                    rulesByPhase[phase].push(rule);
                }
            });
        }

        var html = '<div class="attack-flow">';

        PHASE_ORDER.forEach(function (phase, i) {
            var info = PHASE_INFO[phase];
            var isActive = activePhases.indexOf(phase) !== -1;
            var mapping = phaseMapping[phase];
            var rules = rulesByPhase[phase] || [];

            html += '<div class="af-phase' + (isActive ? '' : ' inactive') + '">';
            html += '<div class="af-phase-header" style="border-color: ' + info.color + '">';
            html += '<span class="af-phase-dot" style="background: ' + info.color + '"></span>';
            html += '<span class="af-phase-label">' + info.label + '</span>';
            html += '<span class="af-phase-name">' + info.name + '</span>';
            html += '</div>';

            if (isActive && mapping && mapping.techniques.length > 0) {
                html += '<div class="af-techniques">';
                mapping.techniques.forEach(function (tech) {
                    html += '<div class="af-technique" data-phase="' + phase + '" title="' + escapeHtml(tech.name) + '">';
                    html += '<span class="af-tech-name">' + escapeHtml(tech.name) + '</span>';
                    html += '</div>';
                });
                html += '</div>';
            } else if (isActive) {
                html += '<div class="af-techniques"><div class="af-technique af-placeholder">Active</div></div>';
            }

            // Detection rule badges
            html += '<div class="af-rules" data-phase="' + phase + '">';
            if (rules.length > 0) {
                rules.forEach(function (rule) {
                    var dlId = rule.dl_id || rule.id || '';
                    html += '<span class="af-rule-badge" title="' + escapeHtml(rule.title || dlId) + '">';
                    html += '<svg class="af-rule-icon" viewBox="0 0 16 16" width="10" height="10"><path d="M8 1l6 3v4c0 3.3-2.6 6.4-6 7.5C4.6 14.4 2 11.3 2 8V4l6-3z" fill="currentColor"/></svg> ';
                    html += escapeHtml(dlId);
                    html += '</span>';
                });
            }
            html += '</div>';

            html += '</div>'; // close af-phase

            // Connector arrow between phases
            if (i < PHASE_ORDER.length - 1) {
                html += '<div class="af-connector' + (isActive ? ' active' : '') + '">';
                html += '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
                html += '</div>';
            }
        });

        html += '</div>';
        container.innerHTML = html;

        // Bind click-to-scroll on technique boxes
        container.querySelectorAll('.af-technique').forEach(function (el) {
            el.addEventListener('click', function () {
                var phase = el.dataset.phase;
                if (!phase) return;
                var phaseNum = phase.replace('P', '');
                var headings = document.querySelectorAll('#detail-body h3');
                for (var j = 0; j < headings.length; j++) {
                    if (headings[j].textContent.indexOf('Phase ' + phaseNum) !== -1) {
                        headings[j].scrollIntoView({ behavior: 'smooth', block: 'start' });
                        break;
                    }
                }
            });
        });
    }

    function updateAttackFlowRules(rules) {
        if (!rules || rules.length === 0) return;

        var rulesByPhase = {};
        rules.forEach(function (rule) {
            var phase = rule.cfpf_phase;
            if (phase) {
                if (!rulesByPhase[phase]) rulesByPhase[phase] = [];
                rulesByPhase[phase].push(rule);
            }
        });

        PHASE_ORDER.forEach(function (phase) {
            var container = document.querySelector('.af-rules[data-phase="' + phase + '"]');
            if (!container) return;
            var phaseRules = rulesByPhase[phase] || [];
            if (phaseRules.length === 0) return;
            var html = '';
            phaseRules.forEach(function (rule) {
                var dlId = rule.dl_id || rule.id || '';
                html += '<span class="af-rule-badge" title="' + escapeHtml(rule.title || dlId) + '">';
                html += '<svg class="af-rule-icon" viewBox="0 0 16 16" width="10" height="10"><path d="M8 1l6 3v4c0 3.3-2.6 6.4-6 7.5C4.6 14.4 2 11.3 2 8V4l6-3z" fill="currentColor"/></svg> ';
                html += escapeHtml(dlId);
                html += '</span>';
            });
            container.innerHTML = html;
        });
    }

    // -------------------------------------------------------------------
    // Component 2: Per-TP Ego Neighborhood Graph
    // -------------------------------------------------------------------

    function renderEgoGraph(container, tpId, options) {
        if (!container || !_data || !tpId) return;
        options = options || {};

        var centerTP = _data.find(function (tp) { return tp.id === tpId; });
        if (!centerTP) return;

        container.innerHTML = '';
        var maxHops = options.maxHops || 1;
        var onNavigate = options.onNavigate || function () {};

        // Collect neighbors and links
        var neighborMap = {};
        var egoLinks = [];
        var linkSet = {};

        function addLink(src, tgt, rel, hop) {
            var key = src + '->' + tgt + ':' + rel;
            if (linkSet[key]) return;
            linkSet[key] = true;
            egoLinks.push({ source: src, target: tgt, relationship: rel, hop: hop || 1 });
        }

        // Forward links from center
        (centerTP.related_tps || []).forEach(function (rel) {
            if (_data.find(function (t) { return t.id === rel.id; })) {
                neighborMap[rel.id] = 1;
                addLink(tpId, rel.id, rel.relationship, 1);
            }
        });

        // Reverse links to center
        (_reverseRelIndex[tpId] || []).forEach(function (rev) {
            if (_data.find(function (t) { return t.id === rev.id; })) {
                neighborMap[rev.id] = 1;
                addLink(rev.id, tpId, rev.relationship, 1);
            }
        });

        // 2-hop expansion
        if (maxHops >= 2) {
            var hop1Ids = Object.keys(neighborMap);
            hop1Ids.forEach(function (nId) {
                var nTP = _data.find(function (t) { return t.id === nId; });
                if (!nTP) return;
                (nTP.related_tps || []).forEach(function (rel) {
                    if (rel.id !== tpId && !neighborMap[rel.id] && _data.find(function (t) { return t.id === rel.id; })) {
                        neighborMap[rel.id] = 2;
                        addLink(nId, rel.id, rel.relationship, 2);
                    }
                });
                (_reverseRelIndex[nId] || []).forEach(function (rev) {
                    if (rev.id !== tpId && !neighborMap[rev.id] && _data.find(function (t) { return t.id === rev.id; })) {
                        neighborMap[rev.id] = 2;
                        addLink(rev.id, nId, rev.relationship, 2);
                    }
                });
            });
        }

        // Build nodes
        var nodes = [{ id: tpId, title: centerTP.title, isCenter: true, hop: 0,
                       sector: (centerTP.sectors || [])[0] || 'other' }];
        Object.keys(neighborMap).forEach(function (nId) {
            var nTP = _data.find(function (t) { return t.id === nId; });
            if (nTP) {
                nodes.push({ id: nId, title: nTP.title, isCenter: false, hop: neighborMap[nId],
                              sector: (nTP.sectors || [])[0] || 'other' });
            }
        });

        if (nodes.length <= 1) {
            container.innerHTML = '<div class="ego-empty">No relationships found for this threat path.</div>';
            return;
        }

        // D3 force simulation
        var width = container.clientWidth || 600;
        var height = 400;

        var svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('viewBox', '0 0 ' + width + ' ' + height);

        var g = svg.append('g');

        // Zoom
        var zoom = d3.zoom()
            .scaleExtent([0.3, 3])
            .on('zoom', function (event) { g.attr('transform', event.transform); });
        svg.call(zoom);

        // Arrow markers
        var defs = svg.append('defs');
        Object.keys(REL_COLORS).forEach(function (rel) {
            defs.append('marker')
                .attr('id', 'ego-arrow-' + rel.replace(/\s/g, '-'))
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 22)
                .attr('refY', 0)
                .attr('markerWidth', 5)
                .attr('markerHeight', 5)
                .attr('orient', 'auto')
                .append('path')
                .attr('d', 'M0,-4L8,0L0,4')
                .attr('fill', REL_COLORS[rel]);
        });
        // Reverse relationship markers
        Object.keys(REL_REVERSE).forEach(function (origRel) {
            var revRel = REL_REVERSE[origRel];
            if (!REL_COLORS[revRel]) {
                defs.append('marker')
                    .attr('id', 'ego-arrow-' + revRel.replace(/\s/g, '-'))
                    .attr('viewBox', '0 -5 10 10')
                    .attr('refX', 22)
                    .attr('refY', 0)
                    .attr('markerWidth', 5)
                    .attr('markerHeight', 5)
                    .attr('orient', 'auto')
                    .append('path')
                    .attr('d', 'M0,-4L8,0L0,4')
                    .attr('fill', REL_COLORS[origRel] || '#6b7280');
            }
        });

        // Force simulation
        var simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(egoLinks).id(function (d) { return d.id; }).distance(100))
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(function (d) { return d.isCenter ? 30 : 20; }));

        // Draw links as curved paths
        var link = g.append('g').attr('class', 'ego-links')
            .selectAll('path').data(egoLinks).enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', function (d) { return REL_COLORS[d.relationship] || REL_COLORS['related-to'] || '#6b7280'; })
            .attr('stroke-width', function (d) { return d.hop > 1 ? 1 : 1.5; })
            .attr('stroke-opacity', function (d) { return d.hop > 1 ? 0.4 : 0.7; })
            .attr('marker-end', function (d) {
                var rel = d.relationship || 'related-to';
                return 'url(#ego-arrow-' + rel.replace(/\s/g, '-') + ')';
            });

        // Draw nodes
        var node = g.append('g').attr('class', 'ego-nodes')
            .selectAll('g').data(nodes).enter().append('g')
            .attr('cursor', 'pointer')
            .call(d3.drag()
                .on('start', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x; d.fy = d.y;
                })
                .on('drag', function (event, d) { d.fx = event.x; d.fy = event.y; })
                .on('end', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null; d.fy = null;
                })
            );

        // Center node glow
        node.filter(function (d) { return d.isCenter; })
            .append('circle')
            .attr('r', 22)
            .attr('fill', 'none')
            .attr('stroke', 'rgba(192, 39, 45, 0.3)')
            .attr('stroke-width', 3)
            .attr('class', 'ego-glow');

        node.append('circle')
            .attr('r', function (d) { return d.isCenter ? 16 : (d.hop > 1 ? 7 : 10); })
            .attr('fill', function (d) { return _sectorColorMap[d.sector] || '#6b7280'; })
            .attr('stroke', function (d) { return d.isCenter ? '#C0272D' : '#000'; })
            .attr('stroke-width', function (d) { return d.isCenter ? 2.5 : 1; })
            .attr('opacity', function (d) { return d.hop > 1 ? 0.6 : 1; });

        node.append('text')
            .attr('class', 'ego-node-label')
            .attr('dx', function (d) { return d.isCenter ? 0 : 14; })
            .attr('dy', function (d) { return d.isCenter ? -22 : 4; })
            .attr('text-anchor', function (d) { return d.isCenter ? 'middle' : 'start'; })
            .attr('font-weight', function (d) { return d.isCenter ? '700' : '500'; })
            .attr('font-size', function (d) { return d.isCenter ? '12px' : '11px'; })
            .attr('fill', function (d) { return d.isCenter ? '#f1f5f9' : '#e2e8f0'; })
            .attr('stroke', 'rgba(0,0,0,0.7)')
            .attr('stroke-width', 2.5)
            .attr('paint-order', 'stroke')
            .attr('opacity', function (d) { return d.hop > 1 ? 0.5 : 1; })
            .text(function (d) { return d.isCenter ? d.title : d.id; });

        // Tooltip
        var tooltip = d3.select(container)
            .append('div')
            .attr('class', 'ego-tooltip')
            .style('display', 'none');

        node.on('mouseover', function (event, d) {
            if (d.isCenter) return;
            tooltip.style('display', 'block')
                .html('<strong>' + escapeHtml(d.id) + '</strong><br>' + escapeHtml(d.title));
            // Highlight connected links
            link.attr('stroke-opacity', function (l) {
                return (l.source.id === d.id || l.target.id === d.id) ? 1 : 0.15;
            });
        })
        .on('mousemove', function (event) {
            var rect = container.getBoundingClientRect();
            tooltip.style('left', (event.clientX - rect.left + 12) + 'px')
                .style('top', (event.clientY - rect.top - 10) + 'px');
        })
        .on('mouseout', function () {
            tooltip.style('display', 'none');
            link.attr('stroke-opacity', function (d) { return d.hop > 1 ? 0.4 : 0.7; });
        })
        .on('click', function (event, d) {
            if (d.isCenter || event.defaultPrevented) return;
            onNavigate(d.id);
        });

        // Link labels on hover
        var linkLabel = g.append('g').attr('class', 'ego-link-labels')
            .selectAll('text').data(egoLinks).enter().append('text')
            .attr('class', 'ego-link-label')
            .attr('text-anchor', 'middle')
            .attr('font-size', '8px')
            .attr('fill', '#888')
            .attr('opacity', 0)
            .text(function (d) { return formatLabel(d.relationship); });

        link.on('mouseover', function (event, d) {
            d3.select(this).attr('stroke-opacity', 1).attr('stroke-width', 2.5);
            linkLabel.filter(function (l) { return l === d; }).attr('opacity', 1);
        }).on('mouseout', function (event, d) {
            d3.select(this).attr('stroke-opacity', d.hop > 1 ? 0.4 : 0.7).attr('stroke-width', d.hop > 1 ? 1 : 1.5);
            linkLabel.filter(function (l) { return l === d; }).attr('opacity', 0);
        });

        // Tick
        simulation.on('tick', function () {
            link.attr('d', function (d) {
                var dx = d.target.x - d.source.x;
                var dy = d.target.y - d.source.y;
                var dr = Math.sqrt(dx * dx + dy * dy) * 1.8;
                return 'M' + d.source.x + ',' + d.source.y + 'A' + dr + ',' + dr + ' 0 0,1 ' + d.target.x + ',' + d.target.y;
            });
            node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
            linkLabel.attr('x', function (d) { return (d.source.x + d.target.x) / 2; })
                .attr('y', function (d) { return (d.source.y + d.target.y) / 2 - 6; });
        });

        // Legend
        var legendDiv = document.createElement('div');
        legendDiv.className = 'ego-legend';
        var legendHtml = '';
        // Only show relationship types present in this graph
        var relTypesUsed = {};
        egoLinks.forEach(function (l) { relTypesUsed[l.relationship] = true; });
        Object.keys(relTypesUsed).forEach(function (rel) {
            var color = REL_COLORS[rel] || REL_COLORS['related-to'] || '#6b7280';
            legendHtml += '<span class="ego-legend-item">';
            legendHtml += '<span class="ego-legend-swatch" style="background:' + color + '"></span>';
            legendHtml += formatLabel(rel);
            legendHtml += '</span>';
        });
        legendDiv.innerHTML = legendHtml;
        container.appendChild(legendDiv);
    }

    // -------------------------------------------------------------------
    // Component 1: Enhanced Global Relationship Graph
    // -------------------------------------------------------------------

    var _globalSimulation = null;

    function renderGlobalGraph(container, legendDiv, controlsDiv, options) {
        if (!container || !_data) return;
        options = options || {};
        var onNavigate = options.onNavigate || function () {};

        container.innerHTML = '';
        if (legendDiv) legendDiv.innerHTML = '';

        var data = _data;

        // Build node and link data
        var nodeMap = {};
        var sectorSet = {};
        var fraudTypeSet = {};
        data.forEach(function (tp) {
            var primarySector = (tp.sectors && tp.sectors.length > 0) ? tp.sectors[0] : 'other';
            sectorSet[primarySector] = true;
            (tp.sectors || []).forEach(function (s) { sectorSet[s] = true; });
            (tp.fraud_types || []).forEach(function (ft) { fraudTypeSet[ft] = true; });
            nodeMap[tp.id] = {
                id: tp.id,
                title: tp.title || tp.id,
                sector: primarySector,
                allSectors: tp.sectors || [],
                fraudTypes: tp.fraud_types || [],
                ruleCount: (tp.detection_rule_ids || []).length,
                phases: (tp.cfpf_phases || []).length,
                pinned: false,
            };
        });

        var sectorList = Object.keys(sectorSet).sort();
        var sectorColorMap = {};
        sectorList.forEach(function (s, i) {
            sectorColorMap[s] = SECTOR_COLORS[i % SECTOR_COLORS.length];
        });

        var fraudTypeList = Object.keys(fraudTypeSet).sort();

        var nodes = Object.values(nodeMap);
        var links = [];
        var linkSet = {};
        data.forEach(function (tp) {
            (tp.related_tps || []).forEach(function (rel) {
                if (nodeMap[rel.id]) {
                    var key = tp.id + '->' + rel.id;
                    if (!linkSet[key]) {
                        linkSet[key] = true;
                        links.push({
                            source: tp.id,
                            target: rel.id,
                            relationship: rel.relationship || 'related-to',
                        });
                    }
                }
            });
        });

        // Check for bidirectional links
        links.forEach(function (l) {
            l.hasBidirectional = linkSet[l.target + '->' + l.source] || false;
        });

        // SVG setup
        var width = container.clientWidth || 800;
        var height = Math.max(container.clientHeight || 550, 550);

        var svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('viewBox', '0 0 ' + width + ' ' + height)
            .attr('id', 'global-graph-svg');

        var g = svg.append('g');

        var zoom = d3.zoom()
            .scaleExtent([0.15, 5])
            .on('zoom', function (event) { g.attr('transform', event.transform); });
        svg.call(zoom);

        // Arrow markers
        var defs = svg.append('defs');
        Object.keys(REL_COLORS).forEach(function (rel) {
            defs.append('marker')
                .attr('id', 'g-arrow-' + rel)
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 20)
                .attr('refY', 0)
                .attr('markerWidth', 5)
                .attr('markerHeight', 5)
                .attr('orient', 'auto')
                .append('path')
                .attr('d', 'M0,-4L8,0L0,4')
                .attr('fill', REL_COLORS[rel]);
        });

        // Sector clustering centers
        var sectorCenters = {};
        sectorList.forEach(function (s, i) {
            var angle = (2 * Math.PI * i) / sectorList.length;
            sectorCenters[s] = {
                x: width / 2 + (width * 0.22) * Math.cos(angle),
                y: height / 2 + (height * 0.22) * Math.sin(angle),
            };
        });

        // Force simulation
        var simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(function (d) { return d.id; }).distance(110))
            .force('charge', d3.forceManyBody().strength(-250))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(function (d) { return 8 + Math.sqrt(d.ruleCount) * 2; }))
            .force('x', d3.forceX(function (d) { return (sectorCenters[d.sector] || { x: width / 2 }).x; }).strength(0.08))
            .force('y', d3.forceY(function (d) { return (sectorCenters[d.sector] || { y: height / 2 }).y; }).strength(0.08));

        _globalSimulation = simulation;

        // Draw links as curved paths
        var link = g.append('g').attr('class', 'graph-links')
            .selectAll('path').data(links).enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', function (d) { return REL_COLORS[d.relationship] || '#6b7280'; })
            .attr('stroke-width', 1.5)
            .attr('stroke-opacity', 0.5)
            .attr('marker-end', function (d) { return 'url(#g-arrow-' + (d.relationship || 'related-to') + ')'; });

        // Draw nodes
        var node = g.append('g').attr('class', 'graph-nodes')
            .selectAll('g').data(nodes).enter().append('g')
            .attr('cursor', 'pointer')
            .call(d3.drag()
                .on('start', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x; d.fy = d.y;
                })
                .on('drag', function (event, d) { d.fx = event.x; d.fy = event.y; })
                .on('end', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.pinned = true;
                    // fx/fy stay set = pinned
                    d3.select(this).select('.graph-node-circle')
                        .attr('stroke-dasharray', '3,2');
                })
            );

        node.append('circle')
            .attr('class', 'graph-node-circle')
            .attr('r', function (d) { return 6 + Math.sqrt(d.ruleCount) * 2; })
            .attr('fill', function (d) { return sectorColorMap[d.sector] || '#6b7280'; })
            .attr('stroke', '#000')
            .attr('stroke-width', 1);

        node.append('text')
            .attr('class', 'graph-node-label')
            .attr('dx', function (d) { return 8 + Math.sqrt(d.ruleCount) * 2; })
            .attr('dy', 4)
            .text(function (d) { return d.id; });

        // Enhanced tooltip
        var tooltip = d3.select(container)
            .append('div')
            .attr('class', 'graph-tooltip')
            .style('display', 'none');

        node.on('mouseover', function (event, d) {
            var ftPreview = d.fraudTypes.slice(0, 3).map(formatLabel).join(', ');
            if (d.fraudTypes.length > 3) ftPreview += ' +' + (d.fraudTypes.length - 3);
            tooltip.style('display', 'block')
                .html(
                    '<div class="gt-header">' + escapeHtml(d.id) + '</div>' +
                    '<div class="gt-title">' + escapeHtml(d.title) + '</div>' +
                    '<div class="gt-meta">' +
                    '<span>Sectors: ' + d.allSectors.map(formatLabel).join(', ') + '</span>' +
                    '<span>Fraud Types: ' + ftPreview + '</span>' +
                    '<span>Detection Rules: ' + d.ruleCount + '</span>' +
                    '</div>'
                );
            link.attr('stroke-opacity', function (l) {
                return (l.source.id === d.id || l.target.id === d.id) ? 1 : 0.1;
            }).attr('stroke-width', function (l) {
                return (l.source.id === d.id || l.target.id === d.id) ? 2.5 : 1;
            });
            node.selectAll('.graph-node-circle').attr('opacity', function (n) {
                if (n.id === d.id) return 1;
                var connected = links.some(function (l) {
                    return (l.source.id === d.id && l.target.id === n.id) ||
                           (l.target.id === d.id && l.source.id === n.id);
                });
                return connected ? 1 : 0.25;
            });
            node.selectAll('.graph-node-label').attr('opacity', function (n) {
                if (n.id === d.id) return 1;
                var connected = links.some(function (l) {
                    return (l.source.id === d.id && l.target.id === n.id) ||
                           (l.target.id === d.id && l.source.id === n.id);
                });
                return connected ? 1 : 0.15;
            });
        })
        .on('mousemove', function (event) {
            var rect = container.getBoundingClientRect();
            tooltip.style('left', (event.clientX - rect.left + 15) + 'px')
                .style('top', (event.clientY - rect.top - 12) + 'px');
        })
        .on('mouseout', function () {
            tooltip.style('display', 'none');
            link.attr('stroke-opacity', 0.5).attr('stroke-width', 1.5);
            node.selectAll('.graph-node-circle').attr('opacity', 1);
            node.selectAll('.graph-node-label').attr('opacity', 1);
        });

        // Click: unpin or navigate
        node.on('click', function (event, d) {
            if (event.defaultPrevented) return;
            if (d.pinned) {
                d.pinned = false;
                d.fx = null;
                d.fy = null;
                simulation.alpha(0.1).restart();
                d3.select(this).select('.graph-node-circle').attr('stroke-dasharray', null);
            }
        });

        // Double-click: navigate
        node.on('dblclick', function (event, d) {
            event.preventDefault();
            onNavigate(d.id);
        });

        // Tick
        simulation.on('tick', function () {
            link.attr('d', function (d) {
                var dx = d.target.x - d.source.x;
                var dy = d.target.y - d.source.y;
                var dr = Math.sqrt(dx * dx + dy * dy) * (d.hasBidirectional ? 1.2 : 2.5);
                var sweep = d.hasBidirectional && (d.source.id > d.target.id) ? 0 : 1;
                return 'M' + d.source.x + ',' + d.source.y + 'A' + dr + ',' + dr + ' 0 0,' + sweep + ' ' + d.target.x + ',' + d.target.y;
            });
            node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        });

        // --- Filter Controls ---
        if (controlsDiv) {
            var filterHtml = '<div class="graph-filter-row">';

            // Relationship type toggles
            filterHtml += '<div class="graph-filter-group"><span class="graph-filter-label">Links:</span>';
            Object.keys(REL_COLORS).forEach(function (rel) {
                filterHtml += '<button class="rel-toggle active" data-rel="' + rel + '" style="border-color:' + REL_COLORS[rel] + '; color:' + REL_COLORS[rel] + '">';
                filterHtml += formatLabel(rel);
                filterHtml += '</button>';
            });
            filterHtml += '</div>';

            // Sector filter
            filterHtml += '<div class="graph-filter-group"><span class="graph-filter-label">Sector:</span>';
            filterHtml += '<select id="graph-sector-filter" class="graph-filter-select">';
            filterHtml += '<option value="">All Sectors</option>';
            sectorList.forEach(function (s) {
                filterHtml += '<option value="' + s + '">' + formatLabel(s) + '</option>';
            });
            filterHtml += '</select></div>';

            // Fraud type filter
            filterHtml += '<div class="graph-filter-group"><span class="graph-filter-label">Fraud:</span>';
            filterHtml += '<select id="graph-fraud-filter" class="graph-filter-select">';
            filterHtml += '<option value="">All Types</option>';
            fraudTypeList.forEach(function (ft) {
                filterHtml += '<option value="' + ft + '">' + formatLabel(ft) + '</option>';
            });
            filterHtml += '</select></div>';

            filterHtml += '</div>';
            controlsDiv.innerHTML = filterHtml;

            // Filter state
            var activeRels = new Set(Object.keys(REL_COLORS));
            var activeSector = '';
            var activeFraudType = '';

            function applyFilters() {
                link.attr('display', function (d) {
                    return activeRels.has(d.relationship) ? null : 'none';
                });
                node.selectAll('.graph-node-circle').attr('opacity', function (d) {
                    if (activeSector && d.allSectors.indexOf(activeSector) === -1) return 0.1;
                    if (activeFraudType && d.fraudTypes.indexOf(activeFraudType) === -1) return 0.1;
                    return 1;
                });
                node.selectAll('.graph-node-label').attr('opacity', function (d) {
                    if (activeSector && d.allSectors.indexOf(activeSector) === -1) return 0.05;
                    if (activeFraudType && d.fraudTypes.indexOf(activeFraudType) === -1) return 0.05;
                    return 1;
                });
            }

            // Bind toggle clicks
            controlsDiv.querySelectorAll('.rel-toggle').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var rel = btn.dataset.rel;
                    if (activeRels.has(rel)) {
                        activeRels.delete(rel);
                        btn.classList.remove('active');
                    } else {
                        activeRels.add(rel);
                        btn.classList.add('active');
                    }
                    applyFilters();
                });
            });

            var sectorSelect = controlsDiv.querySelector('#graph-sector-filter');
            if (sectorSelect) {
                sectorSelect.addEventListener('change', function () {
                    activeSector = this.value;
                    applyFilters();
                });
            }

            var fraudSelect = controlsDiv.querySelector('#graph-fraud-filter');
            if (fraudSelect) {
                fraudSelect.addEventListener('change', function () {
                    activeFraudType = this.value;
                    applyFilters();
                });
            }
        }

        // --- Search ---
        var searchInput = document.getElementById('graph-search');
        if (searchInput) {
            var searchTimer = null;
            searchInput.addEventListener('input', function () {
                clearTimeout(searchTimer);
                var query = searchInput.value.trim().toLowerCase();
                searchTimer = setTimeout(function () {
                    if (!query) {
                        node.selectAll('.graph-node-circle').classed('graph-pulse', false).attr('opacity', 1);
                        node.selectAll('.graph-node-label').attr('opacity', 1);
                        return;
                    }
                    var matchIds = [];
                    nodes.forEach(function (n) {
                        if (n.id.toLowerCase().indexOf(query) !== -1 || n.title.toLowerCase().indexOf(query) !== -1) {
                            matchIds.push(n.id);
                        }
                    });
                    node.selectAll('.graph-node-circle')
                        .classed('graph-pulse', function (d) { return matchIds.indexOf(d.id) !== -1; })
                        .attr('opacity', function (d) { return matchIds.indexOf(d.id) !== -1 ? 1 : 0.15; });
                    node.selectAll('.graph-node-label')
                        .attr('opacity', function (d) { return matchIds.indexOf(d.id) !== -1 ? 1 : 0.08; });
                    // Auto-center on single match
                    if (matchIds.length === 1) {
                        var matchNode = nodes.find(function (n) { return n.id === matchIds[0]; });
                        if (matchNode) {
                            svg.transition().duration(500).call(
                                zoom.transform,
                                d3.zoomIdentity.translate(width / 2 - matchNode.x * 1.5, height / 2 - matchNode.y * 1.5).scale(1.5)
                            );
                        }
                    }
                }, 200);
            });
        }

        // --- Fullscreen ---
        var fullscreenBtn = document.getElementById('graph-fullscreen-btn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', function () {
                var modal = document.getElementById('graph-modal-content');
                if (modal) {
                    modal.classList.toggle('graph-fullscreen');
                    // Resize SVG
                    setTimeout(function () {
                        var newW = container.clientWidth || 800;
                        var newH = container.clientHeight || 550;
                        svg.attr('width', newW).attr('height', newH)
                            .attr('viewBox', '0 0 ' + newW + ' ' + newH);
                        simulation.force('center', d3.forceCenter(newW / 2, newH / 2));
                        simulation.alpha(0.1).restart();
                    }, 100);
                }
            });
        }

        // --- SVG Export ---
        var exportBtn = document.getElementById('graph-export-svg');
        if (exportBtn) {
            exportBtn.addEventListener('click', function () {
                var svgEl = container.querySelector('svg');
                if (svgEl) exportSVG(svgEl, 'flame-relationship-graph.svg');
            });
        }

        // --- Legend ---
        if (legendDiv) {
            var lHtml = '';
            Object.keys(REL_COLORS).forEach(function (rel) {
                lHtml += '<span class="graph-legend-item">';
                lHtml += '<span class="graph-legend-swatch" style="background:' + REL_COLORS[rel] + '"></span>';
                lHtml += formatLabel(rel);
                lHtml += '</span>';
            });
            lHtml += '<span class="graph-legend-sep">|</span>';
            lHtml += '<span class="graph-legend-item" style="font-weight:600">Sectors:</span>';
            sectorList.forEach(function (s) {
                lHtml += '<span class="graph-legend-item">';
                lHtml += '<span class="graph-legend-swatch" style="background:' + sectorColorMap[s] + '; border-radius:50%"></span>';
                lHtml += formatLabel(s);
                lHtml += '</span>';
            });
            legendDiv.innerHTML = lHtml;
        }
    }

    // -------------------------------------------------------------------
    // Public API
    // -------------------------------------------------------------------

    return {
        init: buildReverseRelationshipIndex,
        exportSVG: exportSVG,
        renderAttackFlow: renderAttackFlow,
        updateAttackFlowRules: updateAttackFlowRules,
        renderEgoGraph: renderEgoGraph,
        renderGlobalGraph: renderGlobalGraph,
        REL_COLORS: REL_COLORS,
        SECTOR_COLORS: SECTOR_COLORS,
    };
})();
