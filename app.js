/**
 * app.js - FLAME Frontend Application v2
 *
 * Search-driven discovery interface with card grid, lazy-loaded detail view,
 * heat map, taxonomy toggle, and URL hash routing.
 */

(function () {
    'use strict';

    // -----------------------------------------------------------------------
    // Constants
    // -----------------------------------------------------------------------

    const PHASE_INFO = {
        P1: { label: 'P1', name: 'Recon', color: '#f97316' },
        P2: { label: 'P2', name: 'Initial Access', color: '#ef4444' },
        P3: { label: 'P3', name: 'Positioning', color: '#a855f7' },
        P4: { label: 'P4', name: 'Execution', color: '#3b82f6' },
        P5: { label: 'P5', name: 'Monetization', color: '#22c55e' },
    };

    const PHASE_ORDER = ['P1', 'P2', 'P3', 'P4', 'P5'];

    const GROUPIB_STAGES = [
        'Reconnaissance', 'Resource Development', 'Trust Abuse',
        'End-user Interaction', 'Credential Access', 'Account Access',
        'Defence Evasion', 'Perform Fraud', 'Monetization', 'Laundering'
    ];

    // -----------------------------------------------------------------------
    // State
    // -----------------------------------------------------------------------

    let allSubmissions = [];
    let filteredSubmissions = [];
    const activeFilters = {
        cfpf_phases: new Set(),
        sectors: new Set(),
        fraud_types: new Set(),
    };
    let searchQuery = '';
    let activeTaxonomy = 'cfpf';
    let viewState = 'browse'; // 'browse' | 'detail'

    // -----------------------------------------------------------------------
    // DOM References
    // -----------------------------------------------------------------------

    const dom = {};

    function cacheDom() {
        dom.searchInput = document.getElementById('search-input');
        dom.cardGrid = document.getElementById('card-grid');
        dom.resultsBar = document.getElementById('results-bar');
        dom.browseView = document.getElementById('browse-view');
        dom.detailView = document.getElementById('detail-view');
        dom.detailContent = document.getElementById('detail-content');
        dom.backLink = document.getElementById('back-link');
        dom.statTotal = document.getElementById('stat-total');
        dom.statFraudTypes = document.getElementById('stat-fraud-types');
        dom.statSectors = document.getElementById('stat-sectors');
        dom.filterCfpfPhases = document.getElementById('filter-cfpf-phases');
        dom.filterSectors = document.getElementById('filter-sectors');
        dom.filterFraudTypes = document.getElementById('filter-fraud-types');
        dom.filterActions = document.getElementById('filter-actions');
        dom.clearFiltersBtn = document.getElementById('clear-filters-btn');
        dom.filterCount = document.getElementById('filter-count');
        dom.filterToggle = document.getElementById('filter-toggle');
        dom.filterToggleCount = document.getElementById('filter-toggle-count');
        dom.filterPanel = document.getElementById('filter-panel');
        dom.aboutBtn = document.getElementById('about-btn');
        dom.aboutModal = document.getElementById('about-modal');
        dom.aboutClose = document.getElementById('about-close');
        dom.aboutBody = document.getElementById('about-body');
        dom.heatMapBtn = document.getElementById('heat-map-btn');
        dom.heatMapModal = document.getElementById('heat-map-modal');
        dom.heatMapClose = document.getElementById('heat-map-close');
        dom.heatMapBody = document.getElementById('heat-map-body');
        dom.assessBtn = document.getElementById('assess-btn');
        dom.assessModal = document.getElementById('assess-modal');
        dom.assessClose = document.getElementById('assess-close');
        dom.graphBtn = document.getElementById('graph-btn');
        dom.graphModal = document.getElementById('graph-modal');
        dom.graphClose = document.getElementById('graph-close');
        dom.navigatorBtn = document.getElementById('navigator-btn');
        dom.navigatorModal = document.getElementById('navigator-modal');
        dom.navigatorClose = document.getElementById('navigator-close');
        dom.navigatorBody = document.getElementById('navigator-body');
        dom.navigatorTabs = document.getElementById('navigator-tabs');
        dom.contributorsBtn = document.getElementById('contributors-btn');
        dom.contributorsModal = document.getElementById('contributors-modal');
        dom.contributorsClose = document.getElementById('contributors-close');
        dom.contributorsBody = document.getElementById('contributors-body');
    }

    // -----------------------------------------------------------------------
    // Utilities
    // -----------------------------------------------------------------------

    const _ESC_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    const _ESC_RE = /[&<>"']/g;

    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(_ESC_RE, function (ch) { return _ESC_MAP[ch]; });
    }

    function formatLabel(str) {
        if (!str) return '';
        return str.replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    }

    function truncate(str, len) {
        if (!str) return '';
        if (str.length <= len) return str;
        return str.substring(0, len).replace(/\s+\S*$/, '') + '…';
    }

    // -----------------------------------------------------------------------
    // Initialization
    // -----------------------------------------------------------------------

    document.addEventListener('DOMContentLoaded', function () {
        cacheDom();
        bindEvents();

        FlameData.load().then(function (data) {
            allSubmissions = data;
            initializeUI();
            handleRoute();
            // Load search index and regulatory alerts in parallel (non-blocking)
            FlameData.loadSearchIndex();
            FlameData.loadRegulatoryAlerts().then(function () {
                renderRegulatoryPulse();
            });
        }).catch(function (err) {
            dom.cardGrid.innerHTML = '<div class="empty-state">Failed to load data. Please try again.</div>';
            console.error(err);
        });
    });

    function initializeUI() {
        // Update stats
        const stats = FlameData.getStats();
        dom.statTotal.textContent = stats.total;
        dom.statFraudTypes.textContent = stats.fraudTypes;
        dom.statSectors.textContent = stats.sectors;

        // Build filter chips
        buildPhaseChips();
        buildFilterChips('sectors', dom.filterSectors);
        buildFilterChips('fraud_types', dom.filterFraudTypes);

        // Initial render
        applyFilters();
    }

    // -----------------------------------------------------------------------
    // Event Binding
    // -----------------------------------------------------------------------

    function bindEvents() {
        // Search
        dom.searchInput.addEventListener('input', debounce(function () {
            searchQuery = dom.searchInput.value.trim().toLowerCase();
            applyFilters();
        }, 200));

        // Clear filters
        dom.clearFiltersBtn.addEventListener('click', clearAllFilters);

        // Back link
        dom.backLink.addEventListener('click', function (e) {
            e.preventDefault();
            navigateTo('browse');
        });

        // Mobile filter toggle
        dom.filterToggle.addEventListener('click', function () {
            dom.filterPanel.classList.toggle('open');
        });

        // About modal
        dom.aboutBtn.addEventListener('click', function () {
            renderAbout();
            dom.aboutModal.style.display = 'flex';
        });
        dom.aboutClose.addEventListener('click', function () {
            dom.aboutModal.style.display = 'none';
        });
        dom.aboutModal.addEventListener('click', function (e) {
            if (e.target === dom.aboutModal) dom.aboutModal.style.display = 'none';
        });

        // Heat map modal
        dom.heatMapBtn.addEventListener('click', function () {
            renderHeatMap();
            dom.heatMapModal.style.display = 'flex';
        });
        dom.heatMapClose.addEventListener('click', function () {
            dom.heatMapModal.style.display = 'none';
        });
        dom.heatMapModal.addEventListener('click', function (e) {
            if (e.target === dom.heatMapModal) dom.heatMapModal.style.display = 'none';
        });

        // Coverage Assessment
        dom.assessBtn.addEventListener('click', function () {
            dom.assessModal.style.display = 'flex';
            renderCoverageAssessment();
        });
        dom.assessClose.addEventListener('click', function () { dom.assessModal.style.display = 'none'; });
        dom.assessModal.addEventListener('click', function (e) { if (e.target === dom.assessModal) dom.assessModal.style.display = 'none'; });
        document.getElementById('assess-run-btn').addEventListener('click', runCoverageAssessment);

        // Relationship Graph
        dom.graphBtn.addEventListener('click', function () {
            dom.graphModal.style.display = 'flex';
            renderRelationshipGraph();
        });
        dom.graphClose.addEventListener('click', function () { dom.graphModal.style.display = 'none'; });
        dom.graphModal.addEventListener('click', function (e) { if (e.target === dom.graphModal) dom.graphModal.style.display = 'none'; });

        // Framework Navigator
        dom.navigatorBtn.addEventListener('click', function () {
            dom.navigatorModal.style.display = 'flex';
            renderNavigator('cfpf');
        });
        dom.navigatorClose.addEventListener('click', function () { dom.navigatorModal.style.display = 'none'; });
        dom.navigatorModal.addEventListener('click', function (e) { if (e.target === dom.navigatorModal) dom.navigatorModal.style.display = 'none'; });

        // Navigator tab switching
        dom.navigatorTabs.addEventListener('click', function (e) {
            var tab = e.target.closest('.nav-tab');
            if (!tab) return;
            dom.navigatorTabs.querySelectorAll('.nav-tab').forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');
            var framework = tab.getAttribute('data-framework');
            renderNavigator(framework);
            document.getElementById('nav-export-json').style.display = framework === 'attack' ? 'inline-block' : 'none';
        });

        // Contributors modal
        if (dom.contributorsBtn) {
            dom.contributorsBtn.addEventListener('click', function () {
                renderContributorsModal();
                dom.contributorsModal.style.display = 'flex';
            });
        }
        if (dom.contributorsClose) {
            dom.contributorsClose.addEventListener('click', function () {
                dom.contributorsModal.style.display = 'none';
            });
        }
        if (dom.contributorsModal) {
            dom.contributorsModal.addEventListener('click', function (e) {
                if (e.target === dom.contributorsModal) dom.contributorsModal.style.display = 'none';
            });
        }

        // Navigator exports
        document.getElementById('nav-export-svg').addEventListener('click', exportNavigatorSVG);
        document.getElementById('nav-export-json').addEventListener('click', exportNavigatorATTCKJSON);

        // Hash routing
        window.addEventListener('hashchange', handleRoute);
    }

    function debounce(fn, delay) {
        let timer;
        return function () {
            clearTimeout(timer);
            timer = setTimeout(fn, delay);
        };
    }

    // -----------------------------------------------------------------------
    // Routing
    // -----------------------------------------------------------------------

    function handleRoute() {
        const hash = window.location.hash || '#browse';
        if (hash.startsWith('#detail/')) {
            const tpId = hash.replace('#detail/', '');
            showDetailView(tpId);
        } else {
            showBrowseView();
        }
    }

    function navigateTo(target, tpId) {
        if (target === 'browse') {
            window.location.hash = '#browse';
        } else if (target === 'detail' && tpId) {
            window.location.hash = '#detail/' + tpId;
        }
    }

    function showBrowseView() {
        viewState = 'browse';
        dom.browseView.style.display = 'block';
        dom.detailView.style.display = 'none';
        dom.filterPanel.classList.remove('detail-active');
    }

    function showDetailView(tpId) {
        viewState = 'detail';
        dom.browseView.style.display = 'none';
        dom.detailView.style.display = 'block';
        dom.filterPanel.classList.add('detail-active');

        // Show loading skeleton
        dom.detailContent.innerHTML = '<div class="detail-skeleton"><div class="skeleton-line w80"></div><div class="skeleton-line w60"></div><div class="skeleton-line w40"></div><div class="skeleton-block"></div></div>';

        // Lazy load content
        FlameData.loadContent(tpId).then(function (item) {
            renderDetailView(item);
        }).catch(function (err) {
            dom.detailContent.innerHTML = '<div class="empty-state">Failed to load threat path content.</div>';
            console.error(err);
        });
    }

    // -----------------------------------------------------------------------
    // Filter Chips
    // -----------------------------------------------------------------------

    function buildPhaseChips() {
        let html = '';
        PHASE_ORDER.forEach(function (phase) {
            const info = PHASE_INFO[phase];
            html += '<button class="chip phase-chip" data-filter="cfpf_phases" data-value="' + phase + '" style="--chip-color: ' + info.color + '">';
            html += '<span class="chip-dot" style="background: ' + info.color + '"></span>';
            html += info.label + ' ' + info.name;
            html += '</button>';
        });
        dom.filterCfpfPhases.innerHTML = html;

        dom.filterCfpfPhases.querySelectorAll('.chip').forEach(function (btn) {
            btn.addEventListener('click', function () {
                toggleFilter(btn.dataset.filter, btn.dataset.value, btn);
            });
        });
    }

    function buildFilterChips(field, container) {
        const values = FlameData.getUniqueValues(field);
        let html = '';
        values.forEach(function (val) {
            html += '<button class="chip" data-filter="' + field + '" data-value="' + escapeHtml(val) + '">';
            html += formatLabel(val);
            html += '</button>';
        });
        container.innerHTML = html;

        container.querySelectorAll('.chip').forEach(function (btn) {
            btn.addEventListener('click', function () {
                toggleFilter(btn.dataset.filter, btn.dataset.value, btn);
            });
        });
    }

    function toggleFilter(filterType, value, btn) {
        if (activeFilters[filterType].has(value)) {
            activeFilters[filterType].delete(value);
            btn.classList.remove('active');
        } else {
            activeFilters[filterType].add(value);
            btn.classList.add('active');
        }
        updateFilterBadge();
        applyFilters();
    }

    function clearAllFilters() {
        activeFilters.cfpf_phases.clear();
        activeFilters.sectors.clear();
        activeFilters.fraud_types.clear();
        searchQuery = '';
        dom.searchInput.value = '';

        document.querySelectorAll('.chip.active').forEach(function (btn) {
            btn.classList.remove('active');
        });

        updateFilterBadge();
        applyFilters();
    }

    function updateFilterBadge() {
        const count = activeFilters.cfpf_phases.size + activeFilters.sectors.size + activeFilters.fraud_types.size;
        if (count > 0) {
            dom.filterActions.style.display = 'flex';
            dom.filterCount.textContent = count;
            dom.filterToggleCount.textContent = count;
            dom.filterToggleCount.style.display = 'flex';
        } else {
            dom.filterActions.style.display = 'none';
            dom.filterToggleCount.style.display = 'none';
        }
    }

    // -----------------------------------------------------------------------
    // Filtering & Rendering Cards
    // -----------------------------------------------------------------------

    function applyFilters() {
        // If lunr search is available and query is present, get ranked results
        var lunrMatchIds = null;
        if (searchQuery) {
            var lunrResults = FlameData.search(searchQuery);
            if (lunrResults) {
                lunrMatchIds = new Set();
                lunrResults.forEach(function (r) { lunrMatchIds.add(r.ref); });
            }
        }

        filteredSubmissions = allSubmissions.filter(function (item) {
            // Search — use lunr if available, otherwise fall back to substring
            if (searchQuery) {
                if (lunrMatchIds) {
                    if (!lunrMatchIds.has(item.id)) return false;
                } else {
                    var haystack = (
                        (item.title || '') + ' ' +
                        (item.summary || '') + ' ' +
                        (item.id || '') + ' ' +
                        (item.tags || []).join(' ') + ' ' +
                        (item.fraud_types || []).join(' ') + ' ' +
                        (item.sectors || []).join(' ')
                    ).toLowerCase();
                    if (haystack.indexOf(searchQuery) === -1) return false;
                }
            }

            // CFPF phases
            if (activeFilters.cfpf_phases.size > 0) {
                const phases = item.cfpf_phases || [];
                let match = false;
                activeFilters.cfpf_phases.forEach(function (p) {
                    if (phases.indexOf(p) !== -1) match = true;
                });
                if (!match) return false;
            }

            // Sectors
            if (activeFilters.sectors.size > 0) {
                const sectors = item.sectors || [];
                let sMatch = false;
                activeFilters.sectors.forEach(function (s) {
                    if (sectors.indexOf(s) !== -1) sMatch = true;
                });
                if (!sMatch) return false;
            }

            // Fraud types
            if (activeFilters.fraud_types.size > 0) {
                const ft = item.fraud_types || [];
                let ftMatch = false;
                activeFilters.fraud_types.forEach(function (f) {
                    if (ft.indexOf(f) !== -1) ftMatch = true;
                });
                if (!ftMatch) return false;
            }

            return true;
        });

        renderCardGrid();
    }

    function renderCardGrid() {
        dom.resultsBar.textContent = filteredSubmissions.length + ' of ' + allSubmissions.length + ' threat paths';

        if (filteredSubmissions.length === 0) {
            dom.cardGrid.innerHTML = '<div class="empty-state">No matching threat paths found. Try adjusting your filters.</div>';
            return;
        }

        let html = '';
        filteredSubmissions.forEach(function (item, idx) {
            html += renderCard(item, idx);
        });
        dom.cardGrid.innerHTML = html;

        // Bind card clicks
        dom.cardGrid.querySelectorAll('.tp-card').forEach(function (card) {
            card.addEventListener('click', function () {
                navigateTo('detail', card.dataset.id);
            });
            // Keyboard
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navigateTo('detail', card.dataset.id);
                }
            });
        });
    }

    function renderCard(item, idx) {
        const phases = item.cfpf_phases || [];
        const sectors = item.sectors || [];
        const fraudTypes = item.fraud_types || [];
        const summary = truncate(item.summary || '', 160);

        let html = '<div class="tp-card" data-id="' + escapeHtml(item.id) + '" tabindex="0" role="button" style="--delay: ' + (idx * 0.04) + 's">';

        // Card header
        html += '<div class="card-header">';
        html += '<span class="card-id">' + escapeHtml(item.id) + '</span>';
        if (item.confidence_score != null) {
            var confClass = item.confidence_score >= 70 ? 'conf-high' : (item.confidence_score >= 40 ? 'conf-med' : 'conf-low');
            html += '<span class="conf-dot ' + confClass + '" title="Confidence: ' + item.confidence_score + '"></span>';
        }
        html += '<span class="card-date">' + escapeHtml(item.date || '') + '</span>';
        html += '</div>';

        // Title
        html += '<h3 class="card-title">' + escapeHtml(item.title) + '</h3>';

        // Summary
        html += '<p class="card-summary">' + escapeHtml(summary) + '</p>';

        // Phase dots
        html += '<div class="card-phases">';
        PHASE_ORDER.forEach(function (p) {
            var active = phases.indexOf(p) !== -1;
            var info = PHASE_INFO[p];
            html += '<span class="phase-dot' + (active ? ' active' : '') + '" title="' + info.label + ': ' + info.name + '" style="--dot-color: ' + info.color + '">';
            html += info.label;
            html += '</span>';
        });
        html += '</div>';

        // Tags row
        html += '<div class="card-tags">';
        sectors.forEach(function (s) {
            html += '<span class="card-tag sector-tag">' + formatLabel(s) + '</span>';
        });
        fraudTypes.slice(0, 3).forEach(function (ft) {
            html += '<span class="card-tag fraud-tag">' + formatLabel(ft) + '</span>';
        });
        if (fraudTypes.length > 3) {
            html += '<span class="card-tag more-tag">+' + (fraudTypes.length - 3) + '</span>';
        }
        html += '</div>';

        html += '</div>';
        return html;
    }

    // -----------------------------------------------------------------------
    // Detail View
    // -----------------------------------------------------------------------

    function renderDetailView(item) {
        const phases = item.cfpf_phases || [];
        const mitre = item.mitre_attack || [];
        const groupib = item.groupib_stages || [];
        const sectors = item.sectors || [];
        const fraudTypes = item.fraud_types || [];
        const tags = item.tags || [];
        const ft3 = item.ft3_tactics || [];
        const ucff = item.ucff_domains || {};

        let html = '';

        // Header
        html += '<div class="detail-header">';
        html += '<div class="detail-id">' + escapeHtml(item.id) + '</div>';
        html += '<h2 class="detail-title">' + escapeHtml(item.title) + '</h2>';
        html += '<div class="detail-meta">';
        html += '<span><strong>Author:</strong> ' + escapeHtml(item.author || 'Unknown') + '</span>';
        html += '<span><strong>Date:</strong> ' + escapeHtml(item.date || 'N/A') + '</span>';
        html += '<span><strong>TLP:</strong> <span class="tlp-badge">' + escapeHtml(item.tlp || 'WHITE') + '</span></span>';
        if (item.confidence_score != null) {
            var detailConfClass = item.confidence_score >= 70 ? 'conf-high' : (item.confidence_score >= 40 ? 'conf-med' : 'conf-low');
            html += '<span><strong>Confidence:</strong> <span class="conf-badge ' + detailConfClass + '">' + item.confidence_score + '</span>';
            if (item.source_reliability) html += ' (Reliability: ' + escapeHtml(item.source_reliability) + ')';
            if (item.info_credibility) html += ' (Credibility: ' + item.info_credibility + ')';
            html += '</span>';
        }
        html += '</div>';
        if (item.source) {
            html += '<div class="detail-source"><strong>Source:</strong> ';
            if (item.source.startsWith('http')) {
                html += '<a href="' + escapeHtml(item.source) + '" target="_blank" rel="noopener">' + escapeHtml(truncate(item.source, 80)) + '</a>';
            } else {
                html += escapeHtml(item.source);
            }
            html += '</div>';
        }
        html += '</div>';

        // Taxonomy toggle
        html += '<div class="taxonomy-toggle" id="taxonomy-toggle">';
        html += '<button class="tax-btn' + (activeTaxonomy === 'cfpf' ? ' active' : '') + '" data-taxonomy="cfpf">CFPF Phases</button>';
        html += '<button class="tax-btn' + (activeTaxonomy === 'mitre' ? ' active' : '') + '" data-taxonomy="mitre">MITRE ATT&CK</button>';
        html += '<button class="tax-btn' + (activeTaxonomy === 'groupib' ? ' active' : '') + '" data-taxonomy="groupib">Group-IB</button>';
        html += '</div>';

        // Phase timeline / taxonomy view
        if (activeTaxonomy === 'cfpf') {
            html += renderCfpfTimeline(phases);
        } else if (activeTaxonomy === 'mitre') {
            html += renderMitreView(mitre);
        } else if (activeTaxonomy === 'groupib') {
            html += renderGroupibView(groupib);
        }

        // Taxonomy tags
        html += '<div class="detail-taxonomy">';

        if (sectors.length > 0) {
            html += '<div class="tag-group"><h4>Sectors</h4><div class="tag-list">';
            sectors.forEach(function (s) { html += '<span class="detail-tag sector-tag">' + escapeHtml(formatLabel(s)) + '</span>'; });
            html += '</div></div>';
        }
        if (fraudTypes.length > 0) {
            html += '<div class="tag-group"><h4>Fraud Types</h4><div class="tag-list">';
            fraudTypes.forEach(function (ft) { html += '<span class="detail-tag fraud-tag">' + escapeHtml(formatLabel(ft)) + '</span>'; });
            html += '</div></div>';
        }
        if (mitre.length > 0 && activeTaxonomy !== 'mitre') {
            html += '<div class="tag-group"><h4>MITRE ATT&CK</h4><div class="tag-list">';
            mitre.forEach(function (t) { html += '<span class="detail-tag mitre-tag">' + escapeHtml(t) + '</span>'; });
            html += '</div></div>';
        }
        if (groupib.length > 0 && activeTaxonomy !== 'groupib') {
            html += '<div class="tag-group"><h4>Group-IB Stages</h4><div class="tag-list">';
            groupib.forEach(function (s) { html += '<span class="detail-tag groupib-tag">' + escapeHtml(s) + '</span>'; });
            html += '</div></div>';
        }
        if (ft3.length > 0) {
            html += '<div class="tag-group"><h4>Stripe FT3</h4><div class="tag-list">';
            ft3.forEach(function (t) { html += '<span class="detail-tag ft3-tag">' + escapeHtml(t) + '</span>'; });
            html += '</div></div>';
        }
        // UCFF domains — render only domains with non-empty values, in lifecycle order
        const UCFF_ORDER = ['commit', 'assess', 'plan', 'act', 'monitor', 'report', 'improve'];
        const ucffEntries = [];
        UCFF_ORDER.forEach(function (domain) {
            if (ucff[domain] && String(ucff[domain]).trim() !== '') {
                ucffEntries.push({ domain: domain, value: String(ucff[domain]).trim() });
            }
        });
        if (ucffEntries.length > 0) {
            html += '<div class="tag-group"><h4>UCFF Domains</h4><div class="tag-list">';
            ucffEntries.forEach(function (entry) {
                html += '<span class="detail-tag ucff-tag" title="' + escapeHtml(entry.value) + '">' + escapeHtml(entry.domain.toUpperCase()) + '</span>';
            });
            html += '</div></div>';
        }
        // Regulatory refs
        var regRefs = item.regulatory_refs || [];
        if (regRefs.length > 0) {
            html += '<div class="tag-group"><h4>Regulatory Coverage</h4><div class="tag-list">';
            regRefs.forEach(function (ref) {
                var jurisdiction = '';
                if (ref.indexOf('EU-') !== -1 || ref.indexOf('PSD') !== -1 || ref.indexOf('DORA') !== -1 || ref.indexOf('AMLD') !== -1) jurisdiction = 'EU';
                else if (ref.indexOf('UK-') !== -1 || ref.indexOf('FCA') !== -1) jurisdiction = 'UK';
                else if (ref.indexOf('MAS') !== -1) jurisdiction = 'SG';
                else if (ref.indexOf('AU-') !== -1) jurisdiction = 'AU';
                else if (ref.indexOf('FINCEN') !== -1 || ref.indexOf('FFIEC') !== -1 || ref.indexOf('CFPB') !== -1 || ref.indexOf('SEC') !== -1 || ref.indexOf('OCC') !== -1 || ref.indexOf('FBI') !== -1) jurisdiction = 'US';
                else if (ref.indexOf('FATF') !== -1) jurisdiction = 'INTL';

                var jurisdictionClass = jurisdiction ? ' reg-' + jurisdiction.toLowerCase() : '';
                html += '<span class="detail-tag regulatory-tag' + jurisdictionClass + '" title="' + escapeHtml(ref) + '">';
                if (jurisdiction) html += '<span class="reg-jurisdiction">' + jurisdiction + '</span> ';
                html += escapeHtml(ref.replace('REG-', ''));
                html += '</span>';
            });
            html += '</div></div>';
        }
        if (tags.length > 0) {
            html += '<div class="tag-group"><h4>Tags</h4><div class="tag-list">';
            tags.forEach(function (t) { html += '<span class="detail-tag general-tag">' + escapeHtml(t) + '</span>'; });
            html += '</div></div>';
        }

        html += '</div>';

        // Body content (rendered from markdown)
        if (item.body) {
            html += '<div class="detail-body" id="detail-body">';
            html += renderMarkdown(item.body);
            html += '</div>';
        }

        // Detection Logic placeholder
        html += '<div class="dl-section" id="dl-section">';
        html += '<h2 class="dl-section-title">';
        html += '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>';
        html += ' Detection Logic';
        html += '</h2>';
        html += '<div id="dl-rules-container"><div class="dl-loading">Loading detection rules...</div></div>';
        html += '</div>';

        dom.detailContent.innerHTML = html;

        // Post-render hooks
        bindTaxonomyToggle(item);
        addCopyButtons();
        highlightLookLeftRight();
        loadAndRenderDetectionRules(item.id);

        // Scroll to top
        dom.detailView.scrollTop = 0;
        window.scrollTo(0, 0);
    }

    function loadAndRenderDetectionRules(tpId) {
        FlameData.loadDetectionRules(tpId).then(function (rules) {
            var container = document.getElementById('dl-rules-container');
            if (!container) return;

            if (!rules || rules.length === 0) {
                container.innerHTML = '<div class="dl-empty">No detection rules mapped to this threat path yet.</div>';
                return;
            }

            var html = '';
            rules.forEach(function (rule) {
                html += '<div class="dl-rule-card">';
                html += '<div class="dl-rule-header">';
                html += '<span class="dl-rule-id">' + escapeHtml(rule.dl_id || rule.id || '') + '</span>';
                html += '<span class="dl-rule-level dl-level-' + escapeHtml((rule.level || '').toLowerCase()) + '">' + escapeHtml(rule.level || '') + '</span>';
                html += '</div>';
                html += '<h3 class="dl-rule-title">' + escapeHtml(rule.title || '') + '</h3>';
                html += '<p class="dl-rule-desc">' + escapeHtml(rule.description || '') + '</p>';

                // Detection logic code block
                if (rule.detection) {
                    var yamlStr = formatDetectionYaml(rule.detection);
                    html += '<div class="dl-code-wrapper">';
                    html += '<pre class="dl-code"><code>' + escapeHtml(yamlStr) + '</code></pre>';
                    html += '<button class="dl-copy-btn" data-code="' + escapeHtml(yamlStr).replace(/"/g, '&quot;') + '">Copy</button>';
                    html += '</div>';
                }

                // Tags
                if (rule.tags && rule.tags.length > 0) {
                    html += '<div class="dl-rule-tags">';
                    rule.tags.forEach(function (t) {
                        html += '<span class="dl-tag">' + escapeHtml(t) + '</span>';
                    });
                    html += '</div>';
                }

                html += '</div>';
            });

            container.innerHTML = html;

            // Bind copy buttons
            container.querySelectorAll('.dl-copy-btn').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var code = btn.getAttribute('data-code').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
                    navigator.clipboard.writeText(code).then(function () {
                        btn.textContent = 'Copied!';
                        btn.classList.add('copied');
                        setTimeout(function () {
                            btn.textContent = 'Copy';
                            btn.classList.remove('copied');
                        }, 2000);
                    });
                });
            });
        });
    }

    function formatDetectionYaml(detection) {
        var lines = [];
        Object.keys(detection).forEach(function (key) {
            var val = detection[key];
            if (typeof val === 'object' && val !== null && !Array.isArray(val)) {
                lines.push(key + ':');
                Object.keys(val).forEach(function (subKey) {
                    var subVal = val[subKey];
                    if (Array.isArray(subVal)) {
                        lines.push('  ' + subKey + ':');
                        subVal.forEach(function (item) {
                            lines.push('    - ' + JSON.stringify(item));
                        });
                    } else {
                        lines.push('  ' + subKey + ': ' + JSON.stringify(subVal));
                    }
                });
            } else if (Array.isArray(val)) {
                lines.push(key + ':');
                val.forEach(function (item) {
                    lines.push('  - ' + JSON.stringify(item));
                });
            } else {
                lines.push(key + ': ' + JSON.stringify(val));
            }
        });
        return lines.join('\n');
    }

    // -----------------------------------------------------------------------
    // Taxonomy Views
    // -----------------------------------------------------------------------

    function renderCfpfTimeline(phases) {
        let html = '<div class="phase-timeline">';
        PHASE_ORDER.forEach(function (phase, i) {
            const info = PHASE_INFO[phase];
            const active = phases.indexOf(phase) !== -1;
            html += '<div class="timeline-phase' + (active ? ' active' : '') + '">';
            html += '<div class="timeline-dot" style="background: ' + (active ? info.color : 'var(--color-surface-3)') + '"></div>';
            html += '<div class="timeline-label">' + info.label + '</div>';
            html += '<div class="timeline-name">' + info.name + '</div>';
            html += '</div>';
            if (i < PHASE_ORDER.length - 1) {
                html += '<div class="timeline-connector' + (active ? ' active' : '') + '"></div>';
            }
        });
        html += '</div>';
        return html;
    }

    function renderMitreView(techniques) {
        if (techniques.length === 0) {
            return '<div class="taxonomy-empty">No MITRE ATT&CK mappings for this threat path.</div>';
        }
        let html = '<div class="mitre-grid">';
        techniques.forEach(function (t) {
            html += '<a class="mitre-card" href="https://attack.mitre.org/techniques/' + encodeURIComponent(t.replace('.', '/')) + '/" target="_blank" rel="noopener">';
            html += '<span class="mitre-id">' + escapeHtml(t) + '</span>';
            html += '<span class="mitre-link-icon">↗</span>';
            html += '</a>';
        });
        html += '</div>';
        return html;
    }

    function renderGroupibView(stages) {
        if (stages.length === 0) {
            return '<div class="taxonomy-empty">No Group-IB Fraud Matrix mappings for this threat path.</div>';
        }
        let html = '<div class="groupib-stages">';
        GROUPIB_STAGES.forEach(function (stage, i) {
            const active = stages.indexOf(stage) !== -1;
            html += '<div class="groupib-stage' + (active ? ' active' : '') + '">';
            html += '<span class="groupib-num">' + (i + 1) + '</span>';
            html += '<span class="groupib-name">' + escapeHtml(stage) + '</span>';
            html += '</div>';
        });
        html += '</div>';
        return html;
    }

    function bindTaxonomyToggle(item) {
        const toggleEl = document.getElementById('taxonomy-toggle');
        if (!toggleEl) return;
        toggleEl.querySelectorAll('.tax-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                activeTaxonomy = btn.dataset.taxonomy;
                renderDetailView(item);
            });
        });
    }

    // -----------------------------------------------------------------------
    // Markdown Rendering & Enhancements
    // -----------------------------------------------------------------------

    function renderMarkdown(text) {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                headerIds: false,
            });
            return marked.parse(text);
        }
        return '<pre>' + escapeHtml(text) + '</pre>';
    }

    function addCopyButtons() {
        const codeBlocks = dom.detailContent.querySelectorAll('pre');
        codeBlocks.forEach(function (pre) {
            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(pre);

            const btn = document.createElement('button');
            btn.className = 'copy-btn';
            btn.textContent = 'Copy';
            btn.title = 'Copy to clipboard';
            btn.addEventListener('click', function () {
                const code = pre.querySelector('code') || pre;
                navigator.clipboard.writeText(code.textContent).then(function () {
                    btn.textContent = 'Copied!';
                    btn.classList.add('copied');
                    setTimeout(function () {
                        btn.textContent = 'Copy';
                        btn.classList.remove('copied');
                    }, 2000);
                });
            });
            wrapper.appendChild(btn);
        });
    }

    function highlightLookLeftRight() {
        const body = document.getElementById('detail-body');
        if (!body) return;

        // Find the "Look Left / Look Right" heading
        const headings = body.querySelectorAll('h2');
        headings.forEach(function (h) {
            if (h.textContent.indexOf('Look Left') !== -1 || h.textContent.indexOf('Look Right') !== -1) {
                // Wrap the section in a callout
                const section = document.createElement('div');
                section.className = 'look-callout';

                const icon = document.createElement('div');
                icon.className = 'look-callout-icon';
                icon.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';

                h.classList.add('look-heading');
                h.parentNode.insertBefore(section, h);
                section.appendChild(icon);
                section.appendChild(h);

                // Move sibling elements until next h2
                let next = section.nextSibling;
                while (next && !(next.nodeType === 1 && next.tagName === 'H2')) {
                    const toMove = next;
                    next = next.nextSibling;
                    section.appendChild(toMove);
                }
            }
        });
    }

    // -----------------------------------------------------------------------
    // About Modal
    // -----------------------------------------------------------------------

    function renderAbout() {
        var stats = FlameData.getStats();
        var tp = stats.total || 0;
        var sec = stats.sectors || 0;
        var ft = stats.fraudTypes || 0;
        var phases = stats.phaseCoverage || {};
        var phaseCount = Object.keys(phases).length;

        var html = '';

        // Hero
        html += '<div class="about-hero">';
        html += '<span class="about-logo-icon">&#x1F525;</span>';
        html += '<span class="about-title">FLAME</span>';
        html += '<span class="about-version">v1.0 BEACON</span>';
        html += '<p class="about-tagline">Fraud Lifecycle Analysis &amp; Mitigation Exchange</p>';
        html += '</div>';

        // Live stats
        html += '<div class="about-stats-row">';
        html += '<div class="about-stat"><span class="about-stat-value">' + tp + '</span><span class="about-stat-label">Threat Paths</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">' + ft + '</span><span class="about-stat-label">Fraud Types</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">' + sec + '</span><span class="about-stat-label">Sectors</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">' + phaseCount + '</span><span class="about-stat-label">CFPF Phases</span></div>';
        html += '</div>';

        // Overview
        html += '<div class="about-section">';
        html += '<p>FLAME is an open-source, community-driven platform for sharing structured fraud detection intelligence. ';
        html += 'Each threat path maps fraud schemes across multi-framework lifecycles with detection rules, baselines, and confidence scoring &mdash; ';
        html += 'built by practitioners, for practitioners.</p>';
        html += '</div>';

        // Features grid
        html += '<h3>Platform Capabilities</h3>';
        html += '<div class="about-features-grid">';

        var features = [
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                title: 'STIX 2.1 Extension',
                desc: '4 fraud-specific SDOs with TAXII 2.1 endpoints for TIP integration'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
                title: 'MCP Server',
                desc: '7 AI-agent tools for querying fraud intelligence via Claude, Cursor, etc.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
                title: 'MISP Galaxy & Feed',
                desc: 'Subscribable MISP galaxy with 39 cluster entries and per-TP event feed'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="5" cy="12" r="3"/><circle cx="19" cy="5" r="3"/><circle cx="19" cy="19" r="3"/><line x1="8" y1="12" x2="16" y2="5"/><line x1="8" y1="12" x2="16" y2="19"/></svg>',
                title: 'Relationship Graph',
                desc: 'D3.js force-directed visualization of cross-TP relationships'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
                title: 'Regulatory Mapping',
                desc: '15 regulations (PSD3, FFIEC, FATF, etc.) mapped to threat paths'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="3" x2="9" y2="21"/></svg>',
                title: 'Framework Navigator',
                desc: 'Cross-framework coverage matrix across CFPF, FT3, Group-IB, and ATT&CK'
            }
        ];

        features.forEach(function (f) {
            html += '<div class="about-feature-card">';
            html += '<div class="about-feature-icon">' + f.icon + '</div>';
            html += '<div class="about-feature-title">' + f.title + '</div>';
            html += '<div class="about-feature-desc">' + f.desc + '</div>';
            html += '</div>';
        });
        html += '</div>';

        // Supported frameworks
        html += '<h3>Supported Frameworks</h3>';
        html += '<div class="about-frameworks">';
        var frameworks = [
            { name: 'CFPF', color: 'var(--color-p2)' },
            { name: 'MITRE ATT&CK', color: 'var(--color-mitre)' },
            { name: 'Group-IB Fraud Matrix', color: 'var(--color-groupib)' },
            { name: 'Stripe FT3', color: 'var(--color-ft3)' },
            { name: 'UCFF', color: 'var(--color-ucff)' },
            { name: 'STIX 2.1', color: 'var(--color-sector)' }
        ];
        frameworks.forEach(function (fw) {
            html += '<span class="about-fw-badge" style="border-color: ' + fw.color + '; color: ' + fw.color + ';">' + fw.name + '</span>';
        });
        html += '</div>';

        // Roadmap
        html += '<h3>Roadmap</h3>';
        html += '<div class="about-roadmap">';
        var phases = [
            { name: 'Phase 1: IGNITE', desc: 'Core platform, search, detection logic, heat map', status: 'done' },
            { name: 'Phase 2: FORGE', desc: 'API, MCP server, Sigma export, graph, confidence scoring', status: 'done' },
            { name: 'Phase 3: SIGNAL', desc: 'STIX extension, MISP galaxy, TAXII feeds, regulatory mapping, framework navigator', status: 'done' },
            { name: 'Phase 4: BEACON', desc: 'Community contributions, intake pipeline, RSS/webhook feeds, production hardening', status: 'done' },
            { name: 'Phase 5: SIGNAL-RF', desc: 'Recorded Future 2025 integration — 5 new TPs (e-skimmer, purchase scam, digital wallet, card testing, agentic commerce), 12 detection rules, 5 baselines', status: 'current' }
        ];
        phases.forEach(function (p) {
            html += '<div class="about-roadmap-item about-roadmap-' + p.status + '">';
            html += '<span class="about-roadmap-dot"></span>';
            html += '<div>';
            html += '<strong>' + p.name + '</strong>';
            html += '<span class="about-roadmap-desc"> &mdash; ' + p.desc + '</span>';
            html += '</div>';
            html += '</div>';
        });
        html += '</div>';

        // Changelog
        html += '<h3>Recent Milestones</h3>';
        html += '<div class="about-changelog">';
        var changelog = [
            { date: '2026-03', text: 'Phase 5 SIGNAL-RF: Recorded Future 2025 integration — TP-0035 through TP-0039, 12 new detection rules, 5 baselines, 4 new fraud types' },
            { date: '2026-03', text: 'Phase 4 BEACON: RSS feed, 5 emulation playbooks, contributor leaderboard, peer review workflow' },
            { date: '2026-03', text: 'Contributor submission interface with contribute.html and 5 Issue Form templates' },
            { date: '2026-03', text: 'Emulation Playbook schema (EP-XXXX) with CFPF-mapped steps and DL cross-references' },
            { date: '2026-03', text: 'TP-0034 DPRK IT Worker Fraud: 7 detection rules, baseline profile, full CFPF mapping' },
            { date: '2026-03', text: 'STIX 2.1 fraud extension with 4 custom SDOs, TAXII 2.1, MISP galaxy' },
            { date: '2026-03', text: 'Regulatory mapping (15 regulations, 6 jurisdictions), Framework Navigator' },
            { date: '2026-03', text: 'MCP server, static JSON API, Sigma export pipeline' },
            { date: '2026-02', text: 'D3.js relationship graph, coverage assessment, confidence scoring' }
        ];
        changelog.forEach(function (c) {
            html += '<div class="about-changelog-item">';
            html += '<span class="about-changelog-date">' + c.date + '</span>';
            html += '<span class="about-changelog-text">' + c.text + '</span>';
            html += '</div>';
        });
        html += '</div>';

        // Links
        html += '<h3>Resources</h3>';
        html += '<div class="about-links">';
        html += '<a href="https://github.com/elchacal801/flame-fraud" target="_blank" rel="noopener" class="about-link-btn">GitHub</a>';
        html += '<a href="api/v1/threat-paths.json" target="_blank" rel="noopener" class="about-link-btn">JSON API</a>';
        html += '<a href="api/taxii/discovery.json" target="_blank" rel="noopener" class="about-link-btn">TAXII Feed</a>';
        html += '<a href="data/misp/flame-galaxy.json" target="_blank" rel="noopener" class="about-link-btn">MISP Galaxy</a>';
        html += '<a href="database/flame_stix_bundle.json" target="_blank" rel="noopener" class="about-link-btn">STIX Bundle</a>';
        html += '<a href="database/feed.xml" target="_blank" rel="noopener" class="about-link-btn">RSS Feed</a>';
        html += '</div>';

        // License
        html += '<div class="about-license">';
        html += 'MIT License &middot; Built by practitioners, for practitioners.';
        html += '</div>';

        dom.aboutBody.innerHTML = html;
    }

    // -----------------------------------------------------------------------
    // Heat Map
    // -----------------------------------------------------------------------

    function renderHeatMap() {
        const stats = FlameData.getStats();
        const matrix = stats.coverageMatrix || [];

        if (matrix.length === 0) {
            dom.heatMapBody.innerHTML = '<p>No coverage data available.</p>';
            return;
        }

        // Find max count for color scaling
        let maxCount = 0;
        matrix.forEach(function (row) {
            PHASE_ORDER.forEach(function (p) {
                const val = row.phases[p] || 0;
                if (val > maxCount) maxCount = val;
            });
        });

        let html = '<div class="heat-map-grid">';

        // Header row
        html += '<div class="hm-cell hm-corner"></div>';
        PHASE_ORDER.forEach(function (p) {
            var info = PHASE_INFO[p];
            html += '<div class="hm-cell hm-header" style="color: ' + info.color + '">' + info.label + '</div>';
        });

        // Data rows
        matrix.forEach(function (row) {
            html += '<div class="hm-cell hm-label" title="' + escapeHtml(row.fraud_type) + '">' + escapeHtml(formatLabel(row.fraud_type)) + '</div>';
            PHASE_ORDER.forEach(function (p) {
                const count = row.phases[p] || 0;
                const intensity = maxCount > 0 ? count / maxCount : 0;
                const alpha = count > 0 ? 0.15 + (intensity * 0.85) : 0;
                html += '<div class="hm-cell hm-data" style="background: rgba(192, 39, 45, ' + alpha.toFixed(2) + ')" title="' + formatLabel(row.fraud_type) + ' × ' + p + ': ' + count + ' TPs">';
                if (count > 0) html += count;
                html += '</div>';
            });
        });

        html += '</div>';
        dom.heatMapBody.innerHTML = html;
    }

    // -----------------------------------------------------------------------
    // Framework Navigator
    // -----------------------------------------------------------------------

    function renderNavigator(framework) {
        var data = FlameData.getData();
        if (!data || data.length === 0) {
            dom.navigatorBody.innerHTML = '<p>No data available.</p>';
            return;
        }

        var columns = [];
        var getMapping = null;

        switch (framework) {
            case 'cfpf':
                columns = PHASE_ORDER;
                getMapping = function (item) { return item.cfpf_phases || []; };
                break;
            case 'ft3':
                var ft3Set = new Set();
                data.forEach(function (item) {
                    (item.ft3_tactics || []).forEach(function (t) { ft3Set.add(t); });
                });
                columns = Array.from(ft3Set).sort();
                getMapping = function (item) { return item.ft3_tactics || []; };
                break;
            case 'groupib':
                columns = GROUPIB_STAGES;
                getMapping = function (item) { return item.groupib_stages || []; };
                break;
            case 'attack':
                var attackSet = new Set();
                data.forEach(function (item) {
                    (item.mitre_attack || []).forEach(function (t) { attackSet.add(t); });
                });
                columns = Array.from(attackSet).sort();
                getMapping = function (item) { return item.mitre_attack || []; };
                break;
        }

        if (columns.length === 0) {
            dom.navigatorBody.innerHTML = '<p>No mapping data available for this framework.</p>';
            return;
        }

        var html = '<div class="navigator-grid" style="grid-template-columns: 180px repeat(' + columns.length + ', minmax(60px, 1fr));" id="navigator-grid">';

        // Header row
        html += '<div class="nav-cell nav-corner"></div>';
        columns.forEach(function (col) {
            html += '<div class="nav-cell nav-col-header" title="' + escapeHtml(col) + '">' + escapeHtml(col) + '</div>';
        });

        // Data rows
        data.forEach(function (item) {
            var mapping = getMapping(item);
            html += '<div class="nav-cell nav-row-label" title="' + escapeHtml(item.title) + '">';
            html += '<a href="#tp=' + escapeHtml(item.id) + '" class="nav-tp-link">' + escapeHtml(item.id) + '</a>';
            html += '</div>';

            columns.forEach(function (col) {
                var isMapped = mapping.indexOf(col) !== -1;
                var dlCount = (item.detection_rule_ids || []).length;
                var cellClass = 'nav-cell nav-data';
                if (isMapped) {
                    if (dlCount >= 3) cellClass += ' nav-cell-high';
                    else if (dlCount >= 1) cellClass += ' nav-cell-med';
                    else cellClass += ' nav-cell-low';
                } else {
                    cellClass += ' nav-cell-empty';
                }
                html += '<div class="' + cellClass + '" title="' + escapeHtml(item.title) + ' \u00d7 ' + escapeHtml(col) + '" data-tp="' + escapeHtml(item.id) + '"></div>';
            });
        });

        html += '</div>';
        dom.navigatorBody.innerHTML = html;

        // Click-to-navigate
        dom.navigatorBody.querySelectorAll('.nav-data').forEach(function (cell) {
            cell.addEventListener('click', function () {
                var tpId = cell.getAttribute('data-tp');
                if (tpId) {
                    dom.navigatorModal.style.display = 'none';
                    window.location.hash = '#tp=' + tpId;
                }
            });
        });
    }

    function exportNavigatorSVG() {
        var grid = document.getElementById('navigator-grid');
        if (!grid) return;
        var rect = grid.getBoundingClientRect();
        var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + rect.width + '" height="' + rect.height + '">';
        svg += '<foreignObject width="100%" height="100%">';
        svg += '<div xmlns="http://www.w3.org/1999/xhtml">';
        svg += grid.outerHTML;
        svg += '</div></foreignObject></svg>';

        var blob = new Blob([svg], { type: 'image/svg+xml' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'flame-navigator.svg';
        a.click();
        URL.revokeObjectURL(url);
    }

    function exportNavigatorATTCKJSON() {
        var data = FlameData.getData();
        if (!data) return;
        var techniques = [];
        data.forEach(function (item) {
            (item.mitre_attack || []).forEach(function (techId) {
                techniques.push({
                    techniqueID: techId,
                    score: (item.detection_rule_ids || []).length,
                    comment: item.title + ' (' + item.id + ')',
                    color: '',
                    enabled: true,
                });
            });
        });

        var layer = {
            name: 'FLAME Fraud Coverage',
            versions: { layer: '4.5', navigator: '4.9.1', attack: '14' },
            domain: 'enterprise-attack',
            description: 'FLAME fraud threat path coverage mapped to ATT&CK techniques',
            techniques: techniques,
            gradient: { colors: ['#ffffff', '#fbbf24', '#22c55e'], minValue: 0, maxValue: 5 },
        };

        var blob = new Blob([JSON.stringify(layer, null, 2)], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'flame-attack-navigator.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    // -----------------------------------------------------------------------
    // Regulatory Pulse
    // -----------------------------------------------------------------------

    function renderRegulatoryPulse() {
        var alerts = FlameData.getRegulatoryAlerts();
        var drawerBtn = document.getElementById('pulse-toggle-btn');
        var drawer = document.getElementById('reg-drawer');
        var drawerOverlay = document.getElementById('reg-drawer-overlay');
        var drawerClose = document.getElementById('reg-drawer-close');

        if (!drawer || !drawerBtn) return;

        if (!alerts || alerts.length === 0) {
            drawerBtn.style.display = 'none';
            return;
        }

        // Toggling Drawer logic
        function openDrawer() {
            drawer.classList.add('open');
            drawerOverlay.classList.add('show');
            document.body.style.overflow = 'hidden'; // prevent bg scroll
        }

        function closeDrawer() {
            drawer.classList.remove('open');
            drawerOverlay.classList.remove('show');
            document.body.style.overflow = '';
        }

        drawerBtn.addEventListener('click', openDrawer);
        if (drawerClose) drawerClose.addEventListener('click', closeDrawer);
        if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);



        // Build summary stats
        var severityCounts = { high: 0, medium: 0, low: 0 };
        var sourcesSet = {};
        var tpMapped = 0;
        alerts.forEach(function (a) {
            var sev = (a.severity || '').toLowerCase();
            if (severityCounts.hasOwnProperty(sev)) {
                severityCounts[sev]++;
            }
            if (a.source) {
                sourcesSet[a.source] = true;
            }
            if (a.tp_count && a.tp_count > 0) {
                tpMapped++;
            }
        });
        var sourcesActive = Object.keys(sourcesSet).length;

        // Update Header Badge and Drawer Title Badge
        var alertCountText = alerts.length > 99 ? '99+' : alerts.length;
        var headerBadge = document.getElementById('pulse-header-badge');
        var drawerBadge = document.getElementById('reg-drawer-count');

        if (headerBadge) {
            if (alerts.length > 0) {
                headerBadge.textContent = alertCountText;
                headerBadge.style.display = 'inline-flex';
            } else {
                headerBadge.style.display = 'none';
            }
        }
        if (drawerBadge) {
            drawerBadge.textContent = alertCountText;
        }

        // Sort alerts globally (descending date)
        var sortedAlerts = alerts.slice().sort(function (a, b) {
            return (b.date || '').localeCompare(a.date || '');
        });

        // Source Filter Element
        var sourceSelect = document.getElementById('reg-source-select');
        var currentSourceFilter = 'all';

        if (sourceSelect && sourceSelect.options.length <= 1) {
            var uniqueSources = Object.keys(sourcesSet).sort();
            uniqueSources.forEach(function (src) {
                var opt = document.createElement('option');
                opt.value = src;
                opt.textContent = src.toUpperCase();
                sourceSelect.appendChild(opt);
            });
            sourceSelect.addEventListener('change', function (e) {
                currentSourceFilter = e.target.value;
                currentPage = 1;
                renderRegTable();
            });
        }

        // Pagination State
        var currentPage = 1;
        var alertsPerPage = 20;

        function renderRegTable() {
            var filteredAlerts = currentSourceFilter === 'all'
                ? sortedAlerts
                : sortedAlerts.filter(function (a) { return a.source === currentSourceFilter; });

            var totalPages = Math.ceil(filteredAlerts.length / alertsPerPage);
            if (currentPage > totalPages) currentPage = Math.max(1, totalPages);

            var startIndex = (currentPage - 1) * alertsPerPage;
            var endIndex = Math.min(startIndex + alertsPerPage, filteredAlerts.length);
            var pageAlerts = filteredAlerts.slice(startIndex, endIndex);

            var html = '';

            // Rebuild summary row on every render (or keep it static above the table)
            html += '<div class="reg-summary-row">';
            html += '<div class="reg-stat"><div class="label">Total Alerts</div><div class="value">' + alerts.length.toLocaleString() + '</div></div>';
            html += '<div class="reg-stat"><div class="label">High Severity</div><div class="value" style="color: #f87171;">' + severityCounts.high.toLocaleString() + '</div></div>';
            html += '<div class="reg-stat"><div class="label">Sources Active</div><div class="value" style="color: var(--color-accent);">' + sourcesActive + ' / 6</div></div>';
            html += '<div class="reg-stat"><div class="label">TP-Mapped</div><div class="value" style="color: #4ade80;">' + tpMapped.toLocaleString() + '</div></div>';
            html += '</div>';

            html += '<div class="reg-drawer-intro">';
            html += '<p>Recent enforcement actions, advisories, and industry alerts from regulatory bodies (OFAC, FinCEN, SEC, OCC, FBI IC3).</p>';
            html += '<p>Stay informed about emerging fraud trends and regulatory compliance requirements related to the threat paths in the FLAME dataset.</p>';
            html += '</div>';

            html += '<table class="reg-table">';
            html += '<thead><tr><th>Date</th><th>Source</th><th>Title</th><th>Severity</th><th>TPs</th></tr></thead>';
            html += '<tbody>';

            pageAlerts.forEach(function (a, index) {
                var sourceClass = (a.source || '').toLowerCase().replace(/[^a-z0-9_]/g, '_');
                var sevClass = (a.severity || '').toLowerCase();
                var titleText = escapeHtml(truncate(a.title || '', 60));

                // Using dataset attributes and custom classes for the expand logic
                html += '<tr class="reg-row-header" data-index="' + index + '">';
                html += '<td style="white-space:nowrap;">' + escapeHtml(a.date || '—') + '</td>';
                html += '<td><span class="reg-source-badge ' + escapeHtml(sourceClass) + '">' + escapeHtml((a.source || '').toUpperCase()) + '</span></td>';

                // Keep the link if it exists, but prevent row expand when clicking it
                if (a.url) {
                    html += '<td><a href="' + escapeHtml(a.url) + '" target="_blank" rel="noopener" class="reg-link-prevent">' + titleText + '</a></td>';
                } else {
                    html += '<td>' + titleText + '</td>';
                }

                html += '<td><span class="reg-severity-pill ' + escapeHtml(sevClass) + '">' + escapeHtml(a.severity || '') + '</span></td>';
                html += '<td style="text-align:center;">' + escapeHtml(String(a.tp_count != null ? a.tp_count : '—')) + '</td>';
                html += '</tr>';

                // Expanding Context Row
                html += '<tr class="reg-row-detail" id="reg-detail-' + index + '">';
                html += '<td colspan="5">';
                html += '<div class="reg-detail-content">';
                html += '<div style="margin-bottom: 8px;"><strong>Summary:</strong> ' + escapeHtml(a.summary || 'No summary available.') + '</div>';
                if (a.mapped_tp_ids && a.mapped_tp_ids.length > 0) {
                    html += '<div style="margin-top: 4px;"><strong>Relevant TPs:</strong> ' + escapeHtml(a.mapped_tp_ids.join(', ')) + '</div>';
                }
                html += '</div>';
                html += '</td>';
                html += '</tr>';
            });
            html += '</tbody></table>';

            // Pagination Controls
            if (totalPages > 1) {
                html += '<div class="reg-pagination">';
                html += '<button class="reg-page-btn" id="reg-prev-btn" ' + (currentPage === 1 ? 'disabled' : '') + '>Previous</button>';
                html += '<span class="reg-page-info">Page ' + currentPage + ' of ' + totalPages + '</span>';
                html += '<button class="reg-page-btn" id="reg-next-btn" ' + (currentPage === totalPages ? 'disabled' : '') + '>Next</button>';
                html += '</div>';
            } else if (filteredAlerts.length === 0) {
                html += '<div style="padding: var(--space-lg); text-align: center; color: var(--color-text-dim);">No alerts found for this source.</div>';
            }

            var drawerBody = document.getElementById('reg-drawer-body');
            if (drawerBody) {
                drawerBody.innerHTML = html;

                // Re-bind events for the new DOM elements
                var prevBtn = document.getElementById('reg-prev-btn');
                var nextBtn = document.getElementById('reg-next-btn');

                if (prevBtn) {
                    prevBtn.addEventListener('click', function () {
                        if (currentPage > 1) {
                            currentPage--;
                            renderRegTable();
                        }
                    });
                }
                if (nextBtn) {
                    nextBtn.addEventListener('click', function () {
                        if (currentPage < totalPages) {
                            currentPage++;
                            renderRegTable();
                        }
                    });
                }

                // Row expand logic
                var rowHeaders = drawerBody.querySelectorAll('.reg-row-header');
                rowHeaders.forEach(function (row) {
                    row.addEventListener('click', function (e) {
                        // Don't expand if they clicked the outgoing URL link
                        if (e.target.classList.contains('reg-link-prevent')) {
                            return;
                        }
                        var idx = row.getAttribute('data-index');
                        var detailRow = document.getElementById('reg-detail-' + idx);
                        if (detailRow) {
                            detailRow.classList.toggle('open');
                        }
                    });
                });
            }
        }

        // Initial table render
        renderRegTable();

    }

    // -----------------------------------------------------------------------
    // Coverage Self-Assessment
    // -----------------------------------------------------------------------

    function renderCoverageAssessment() {
        // Populate checkboxes from stats
        var stats = FlameData.getStats();
        var sectorsDiv = document.getElementById('assess-sectors');
        var fraudTypesDiv = document.getElementById('assess-fraud-types');

        sectorsDiv.innerHTML = (stats.sectorList || []).map(function (s) {
            return '<label class="assess-check"><input type="checkbox" value="' + escapeHtml(s) + '"> ' + formatLabel(s) + '</label>';
        }).join('');

        fraudTypesDiv.innerHTML = (stats.fraudTypeList || []).map(function (ft) {
            return '<label class="assess-check"><input type="checkbox" value="' + escapeHtml(ft) + '"> ' + formatLabel(ft) + '</label>';
        }).join('');

        // Reset view to selection step
        document.getElementById('assess-selection').style.display = 'block';
        document.getElementById('assess-results').style.display = 'none';
    }

    function runCoverageAssessment() {
        var selectedSectors = Array.from(document.querySelectorAll('#assess-sectors input:checked')).map(function (i) { return i.value; });
        var selectedFraudTypes = Array.from(document.querySelectorAll('#assess-fraud-types input:checked')).map(function (i) { return i.value; });

        if (selectedSectors.length === 0 && selectedFraudTypes.length === 0) {
            alert('Please select at least one sector or fraud type.');
            return;
        }

        var data = FlameData.getData();

        // Filter TPs by selected sectors
        var relevantTPs = data;
        if (selectedSectors.length > 0) {
            relevantTPs = relevantTPs.filter(function (tp) {
                return tp.sectors && tp.sectors.some(function (s) { return selectedSectors.indexOf(s) !== -1; });
            });
        }
        // Further filter by fraud types
        if (selectedFraudTypes.length > 0) {
            relevantTPs = relevantTPs.filter(function (tp) {
                return tp.fraud_types && tp.fraud_types.some(function (ft) { return selectedFraudTypes.indexOf(ft) !== -1; });
            });
        }

        // Coverage per fraud type (phase coverage)
        var coverageByFT = {};
        selectedFraudTypes.forEach(function (ft) {
            var ftTPs = relevantTPs.filter(function (tp) { return tp.fraud_types && tp.fraud_types.indexOf(ft) !== -1; });
            var coveredPhases = {};
            ftTPs.forEach(function (tp) {
                (tp.cfpf_phases || []).forEach(function (p) { coveredPhases[p] = true; });
            });
            var allPhases = ['P1', 'P2', 'P3', 'P4', 'P5'];
            var covered = allPhases.filter(function (p) { return coveredPhases[p]; });
            coverageByFT[ft] = {
                count: ftTPs.length,
                covered: covered,
                gaps: allPhases.filter(function (p) { return !coveredPhases[p]; }),
            };
        });

        // Phase weakness (count TPs per phase)
        var phaseCount = { P1: 0, P2: 0, P3: 0, P4: 0, P5: 0 };
        relevantTPs.forEach(function (tp) {
            (tp.cfpf_phases || []).forEach(function (p) {
                if (phaseCount[p] !== undefined) phaseCount[p]++;
            });
        });
        var maxPhase = Math.max(phaseCount.P1, phaseCount.P2, phaseCount.P3, phaseCount.P4, phaseCount.P5, 1);

        // Coverage score = % of selected fraud types with at least 1 TP
        var coveredFTs = 0;
        Object.keys(coverageByFT).forEach(function (ft) {
            if (coverageByFT[ft].count > 0) coveredFTs++;
        });
        var coverageScore = selectedFraudTypes.length > 0
            ? Math.round(coveredFTs / selectedFraudTypes.length * 100)
            : 0;

        // Average confidence
        var scores = relevantTPs.filter(function (tp) { return tp.confidence_score != null; }).map(function (tp) { return tp.confidence_score; });
        var avgConf = scores.length > 0 ? Math.round(scores.reduce(function (a, b) { return a + b; }, 0) / scores.length) : null;

        // Detection rule count
        var recommendedRuleIds = {};
        relevantTPs.forEach(function (tp) {
            (tp.detection_rule_ids || []).forEach(function (id) { recommendedRuleIds[id] = true; });
        });
        var ruleCount = Object.keys(recommendedRuleIds).length;

        // Render results
        var html = '<button class="assess-back-btn" id="assess-back-btn">\u2190 Back to Selection</button>';

        // Score summary
        html += '<div class="assess-score-row">';
        html += '<div class="assess-score-card">';
        html += '<div class="assess-score-value">' + coverageScore + '%</div>';
        html += '<div class="assess-score-label">Coverage Score</div>';
        html += '</div>';
        html += '<div class="assess-score-card">';
        html += '<div class="assess-score-value">' + relevantTPs.length + '</div>';
        html += '<div class="assess-score-label">Matching Threat Paths</div>';
        html += '</div>';
        html += '<div class="assess-score-card">';
        html += '<div class="assess-score-value">' + ruleCount + '</div>';
        html += '<div class="assess-score-label">Detection Rules</div>';
        html += '</div>';
        if (avgConf !== null) {
            html += '<div class="assess-score-card">';
            html += '<div class="assess-score-value">' + avgConf + '</div>';
            html += '<div class="assess-score-label">Avg Confidence</div>';
            html += '</div>';
        }
        html += '</div>';

        // Phase weakness chart (CSS bar chart)
        html += '<div class="assess-section">';
        html += '<h3>CFPF Phase Coverage</h3>';
        html += '<div class="assess-phase-chart">';
        PHASE_ORDER.forEach(function (p) {
            var pct = maxPhase > 0 ? Math.round(phaseCount[p] / maxPhase * 100) : 0;
            var info = PHASE_INFO[p];
            html += '<div class="assess-phase-bar">';
            html += '<span class="assess-phase-label">' + p + '</span>';
            html += '<div class="assess-bar-track">';
            html += '<div class="assess-bar-fill" style="width: ' + pct + '%; background: ' + info.color + ';"></div>';
            html += '</div>';
            html += '<span class="assess-phase-count">' + phaseCount[p] + '</span>';
            html += '</div>';
        });
        html += '</div></div>';

        // Gap list
        var gapFTs = [];
        Object.keys(coverageByFT).forEach(function (ft) {
            if (coverageByFT[ft].count === 0) gapFTs.push(ft);
        });
        if (gapFTs.length > 0) {
            html += '<div class="assess-section">';
            html += '<h3>Uncovered Fraud Types</h3>';
            html += '<div class="assess-gap-list">';
            gapFTs.forEach(function (ft) {
                html += '<span class="assess-gap-tag">' + formatLabel(ft) + '</span>';
            });
            html += '</div></div>';
        }

        // Coverage table
        var coveredFTEntries = [];
        Object.keys(coverageByFT).forEach(function (ft) {
            if (coverageByFT[ft].count > 0) coveredFTEntries.push([ft, coverageByFT[ft]]);
        });
        if (coveredFTEntries.length > 0) {
            html += '<div class="assess-section">';
            html += '<h3>Fraud Type Coverage Detail</h3>';
            html += '<table class="assess-table"><thead><tr><th>Fraud Type</th><th>TPs</th><th>Phases Covered</th><th>Gaps</th></tr></thead><tbody>';
            coveredFTEntries.forEach(function (entry) {
                var ft = entry[0];
                var c = entry[1];
                html += '<tr>';
                html += '<td>' + formatLabel(ft) + '</td>';
                html += '<td>' + c.count + '</td>';
                html += '<td>' + c.covered.join(', ') + '</td>';
                html += '<td>' + (c.gaps.length > 0 ? c.gaps.join(', ') : '<span style="color:var(--color-success)">Full</span>') + '</td>';
                html += '</tr>';
            });
            html += '</tbody></table></div>';
        }

        document.getElementById('assess-results').innerHTML = html;
        document.getElementById('assess-selection').style.display = 'none';
        document.getElementById('assess-results').style.display = 'block';

        // Back button
        document.getElementById('assess-back-btn').addEventListener('click', function () {
            document.getElementById('assess-selection').style.display = 'block';
            document.getElementById('assess-results').style.display = 'none';
        });
    }

    // -----------------------------------------------------------------------
    // Relationship Graph (D3.js)
    // -----------------------------------------------------------------------

    var REL_COLORS = {
        'feeds-into': '#ef4444',
        'enables': '#3b82f6',
        'enhances': '#a855f7',
        'provides-mules-for': '#22c55e',
        'shares-infrastructure': '#f97316',
        'escalates-from': '#eab308',
        'related-to': '#6b7280',
    };

    var SECTOR_COLORS = [
        '#0ea5e9', '#f43f5e', '#a78bfa', '#34d399', '#fbbf24',
        '#06b6d4', '#fb923c', '#e879f9', '#4ade80', '#f87171'
    ];

    function renderRelationshipGraph() {
        var container = document.getElementById('graph-container');
        var legendDiv = document.getElementById('graph-legend');
        if (!container) return;

        // Clear previous
        container.innerHTML = '';
        legendDiv.innerHTML = '';

        var data = FlameData.getData();
        if (!data || data.length === 0) return;

        // Build node and link data
        var nodeMap = {};
        var sectorSet = {};
        data.forEach(function (tp) {
            var primarySector = (tp.sectors && tp.sectors.length > 0) ? tp.sectors[0] : 'other';
            sectorSet[primarySector] = true;
            nodeMap[tp.id] = {
                id: tp.id,
                title: tp.title || tp.id,
                sector: primarySector,
                confidence: tp.confidence_score,
                phases: (tp.cfpf_phases || []).length,
            };
        });

        var sectorList = Object.keys(sectorSet).sort();
        var sectorColorMap = {};
        sectorList.forEach(function (s, i) {
            sectorColorMap[s] = SECTOR_COLORS[i % SECTOR_COLORS.length];
        });

        var nodes = [];
        Object.keys(nodeMap).forEach(function (id) { nodes.push(nodeMap[id]); });

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

        // SVG setup
        var width = container.clientWidth || 800;
        var height = Math.max(container.clientHeight || 500, 500);

        var svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('viewBox', '0 0 ' + width + ' ' + height);

        // Zoom group
        var g = svg.append('g');

        var zoom = d3.zoom()
            .scaleExtent([0.2, 4])
            .on('zoom', function (event) {
                g.attr('transform', event.transform);
            });

        svg.call(zoom);

        // Arrow markers for each relationship type
        var defs = svg.append('defs');
        Object.keys(REL_COLORS).forEach(function (rel) {
            defs.append('marker')
                .attr('id', 'arrow-' + rel)
                .attr('viewBox', '0 -5 10 10')
                .attr('refX', 20)
                .attr('refY', 0)
                .attr('markerWidth', 6)
                .attr('markerHeight', 6)
                .attr('orient', 'auto')
                .append('path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', REL_COLORS[rel]);
        });

        // Force simulation
        var simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(function (d) { return d.id; }).distance(120))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(30));

        // Draw links
        var link = g.append('g')
            .attr('class', 'graph-links')
            .selectAll('line')
            .data(links)
            .enter()
            .append('line')
            .attr('stroke', function (d) { return REL_COLORS[d.relationship] || REL_COLORS['related-to']; })
            .attr('stroke-width', 1.5)
            .attr('stroke-opacity', 0.6)
            .attr('marker-end', function (d) { return 'url(#arrow-' + (d.relationship || 'related-to') + ')'; });

        // Draw nodes
        var node = g.append('g')
            .attr('class', 'graph-nodes')
            .selectAll('g')
            .data(nodes)
            .enter()
            .append('g')
            .attr('cursor', 'pointer')
            .call(d3.drag()
                .on('start', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                })
                .on('drag', function (event, d) {
                    d.fx = event.x;
                    d.fy = event.y;
                })
                .on('end', function (event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                })
            );

        node.append('circle')
            .attr('r', function (d) { return 6 + (d.phases || 0) * 1.5; })
            .attr('fill', function (d) { return sectorColorMap[d.sector] || '#6b7280'; })
            .attr('stroke', '#000')
            .attr('stroke-width', 1);

        node.append('text')
            .attr('class', 'graph-node-label')
            .attr('dx', 12)
            .attr('dy', 4)
            .text(function (d) { return d.id; });

        // Tooltip
        var tooltip = d3.select(container)
            .append('div')
            .attr('class', 'graph-tooltip')
            .style('display', 'none');

        node.on('mouseover', function (event, d) {
            tooltip.style('display', 'block')
                .html('<strong>' + escapeHtml(d.id) + '</strong><br>' + escapeHtml(d.title));
            // Highlight connected links
            link.attr('stroke-opacity', function (l) {
                return (l.source.id === d.id || l.target.id === d.id) ? 1 : 0.15;
            }).attr('stroke-width', function (l) {
                return (l.source.id === d.id || l.target.id === d.id) ? 2.5 : 1;
            });
        })
        .on('mousemove', function (event) {
            var rect = container.getBoundingClientRect();
            tooltip.style('left', (event.clientX - rect.left + 12) + 'px')
                .style('top', (event.clientY - rect.top - 10) + 'px');
        })
        .on('mouseout', function () {
            tooltip.style('display', 'none');
            link.attr('stroke-opacity', 0.6).attr('stroke-width', 1.5);
        })
        .on('click', function (event, d) {
            // Close modal and navigate to detail view
            dom.graphModal.style.display = 'none';
            navigateTo('detail', d.id);
        });

        // Simulation tick
        simulation.on('tick', function () {
            link
                .attr('x1', function (d) { return d.source.x; })
                .attr('y1', function (d) { return d.source.y; })
                .attr('x2', function (d) { return d.target.x; })
                .attr('y2', function (d) { return d.target.y; });

            node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
        });

        // Legend — relationship types
        var legendHtml = '';
        Object.keys(REL_COLORS).forEach(function (rel) {
            legendHtml += '<span class="graph-legend-item">';
            legendHtml += '<span class="graph-legend-swatch" style="background: ' + REL_COLORS[rel] + ';"></span>';
            legendHtml += formatLabel(rel);
            legendHtml += '</span>';
        });
        // Sector colors
        legendHtml += '<span class="graph-legend-item" style="margin-left: 16px; font-weight: 600;">Sectors:</span>';
        sectorList.forEach(function (s) {
            legendHtml += '<span class="graph-legend-item">';
            legendHtml += '<span class="graph-legend-swatch" style="background: ' + sectorColorMap[s] + '; width: 12px; height: 12px; border-radius: 50%;"></span>';
            legendHtml += formatLabel(s);
            legendHtml += '</span>';
        });
        legendDiv.innerHTML = legendHtml;
    }

    // -----------------------------------------------------------------------
    // Contributors Leaderboard
    // -----------------------------------------------------------------------

    function renderContributorsModal() {
        var body = dom.contributorsBody;
        if (!body) return;

        body.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--color-text-dim);">Loading contributors...</div>';

        fetch('database/flame-contributors.json')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                var contributors = data.contributors || [];
                var html = '';

                // Hero
                html += '<div class="contributors-hero">';
                html += '<span class="contributors-hero-icon">🔥</span>';
                html += '<p class="contributors-hero-tagline">Community contributions powering fraud intelligence</p>';
                html += '</div>';

                // Total
                var totalContribs = 0;
                contributors.forEach(function (c) { totalContribs += c.total; });
                html += '<div class="contributors-total">' + contributors.length + ' contributors &middot; ' + totalContribs + ' total contributions</div>';

                if (contributors.length === 0) {
                    html += '<div style="padding: 2rem; text-align: center; color: var(--color-text-dim);">No contributor data available.</div>';
                } else {
                    html += '<table class="leaderboard-table">';
                    html += '<thead><tr>';
                    html += '<th>Rank</th>';
                    html += '<th>Contributor</th>';
                    html += '<th>TPs</th>';
                    html += '<th>DL Rules</th>';
                    html += '<th>Baselines</th>';
                    html += '<th>EPs</th>';
                    html += '<th>Total</th>';
                    html += '</tr></thead>';
                    html += '<tbody>';

                    contributors.forEach(function (c, i) {
                        html += '<tr>';
                        html += '<td>' + (i + 1) + '</td>';
                        html += '<td>' + escapeHtml(c.name) + '</td>';
                        html += '<td>' + c.threat_paths + '</td>';
                        html += '<td>' + c.detection_rules + '</td>';
                        html += '<td>' + c.baselines + '</td>';
                        html += '<td>' + c.emulation_playbooks + '</td>';
                        html += '<td><strong>' + c.total + '</strong></td>';
                        html += '</tr>';
                    });

                    html += '</tbody></table>';
                }

                body.innerHTML = html;
            })
            .catch(function (err) {
                body.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--color-text-dim);">Failed to load contributor data.</div>';
                console.error('Contributors load error:', err);
            });
    }

    // -----------------------------------------------------------------------
    // End
    // -----------------------------------------------------------------------

})();
