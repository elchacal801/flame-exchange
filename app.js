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
    let viewState = 'browse'; // 'browse' | 'detail' | 'baselines'
    let browseMode = 'matrix'; // 'matrix' | 'grid'
    let matrixSector = 'all';  // active sector tab for matrix view

    const FRAUD_FAMILY_ORDER = [
        'account-takeover', 'payment-wire', 'social-engineering',
        'identity-synthetic', 'investment-romance', 'insurance-healthcare',
        'crypto-laundering', 'fraud-infrastructure', 'retail-ecommerce',
        'state-geopolitical', 'telecom-specialized',
    ];

    const FRAUD_FAMILY_LABELS = {
        'account-takeover': 'Account Takeover & Credential Theft',
        'payment-wire': 'Payment & Wire Fraud',
        'social-engineering': 'Social Engineering & APP',
        'identity-synthetic': 'Identity & Synthetic Fraud',
        'investment-romance': 'Investment & Romance Scams',
        'insurance-healthcare': 'Insurance & Healthcare Fraud',
        'crypto-laundering': 'Crypto & Laundering',
        'fraud-infrastructure': 'Fraud Infrastructure & FaaS',
        'retail-ecommerce': 'Retail & E-Commerce Fraud',
        'state-geopolitical': 'State-Linked & Geopolitical',
        'telecom-specialized': 'Telecom & Specialized Fraud',
    };

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
        dom.ucffBtn = document.getElementById('ucff-btn');
        dom.ucffModal = document.getElementById('ucff-modal');
        dom.ucffClose = document.getElementById('ucff-close');
        dom.ucffSliderPanel = document.getElementById('ucff-slider-panel');
        dom.ucffSummary = document.getElementById('ucff-summary');
        dom.ucffRadar = document.getElementById('ucff-radar');
        dom.ucffGridBody = document.getElementById('ucff-grid-body');
        dom.ucffGrid = document.getElementById('ucff-grid');
        dom.ucffExportBtn = document.getElementById('ucff-export-btn');
        dom.ucffImportBtn = document.getElementById('ucff-import-btn');
        dom.ucffFileInput = document.getElementById('ucff-file-input');
        dom.baselinesView = document.getElementById('baselines-view');
        dom.baselinesGrid = document.getElementById('baselines-grid');
        dom.baselinesSearchInput = document.getElementById('baselines-search-input');
        dom.mainNav = document.getElementById('main-nav');
        dom.matrixView = document.getElementById('matrix-view');
        dom.matrixTable = document.getElementById('matrix-table');
        dom.matrixThead = document.getElementById('matrix-thead');
        dom.matrixTbody = document.getElementById('matrix-tbody');
        dom.matrixSectorTabs = document.getElementById('matrix-sector-tabs');
        dom.viewMatrixBtn = document.getElementById('view-matrix-btn');
        dom.viewGridBtn = document.getElementById('view-grid-btn');
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
    // Theme Toggle
    // -----------------------------------------------------------------------

    function initTheme() {
        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;
        btn.addEventListener('click', function () {
            var current = document.documentElement.getAttribute('data-theme') || 'dark';
            var next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('flame-theme', next);
            var meta = document.querySelector('meta[name="theme-color"]');
            if (meta) meta.setAttribute('content', next === 'light' ? '#F5F3F1' : '#09090B');
        });
    }

    // -----------------------------------------------------------------------
    // Initialization
    // -----------------------------------------------------------------------

    document.addEventListener('DOMContentLoaded', function () {
        cacheDom();
        initTheme();
        bindEvents();

        FlameData.load().then(function (data) {
            allSubmissions = data;
            FlameViz.init(data);
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
        // View toggle (matrix / grid)
        initViewToggle();

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

        // Hamburger menu
        var hamburger = document.getElementById('nav-hamburger');
        if (hamburger) {
            hamburger.addEventListener('click', function() {
                dom.mainNav.classList.toggle('nav-open');
            });
            // Close menu when a tab is clicked
            dom.mainNav.querySelectorAll('.nav-tab').forEach(function(tab) {
                tab.addEventListener('click', function() {
                    dom.mainNav.classList.remove('nav-open');
                });
            });
        }

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
            FlameViz.renderGlobalGraph(
                document.getElementById('graph-container'),
                document.getElementById('graph-legend'),
                document.getElementById('graph-controls'),
                { onNavigate: function (id) { dom.graphModal.style.display = 'none'; navigateTo('detail', id); } }
            );
        });
        dom.graphClose.addEventListener('click', function () { dom.graphModal.style.display = 'none'; });
        dom.graphModal.addEventListener('click', function (e) { if (e.target === dom.graphModal) dom.graphModal.style.display = 'none'; });
        // Fullscreen toggle handled by FlameViz.renderGlobalGraph() in viz.js
        // SVG export handled by FlameViz.renderGlobalGraph() in viz.js

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

        // UCFF Maturity Assessment
        dom.ucffBtn.addEventListener('click', function () {
            dom.ucffModal.style.display = 'flex';
            initUcffAssessment();
        });
        dom.ucffClose.addEventListener('click', function () { dom.ucffModal.style.display = 'none'; });
        dom.ucffModal.addEventListener('click', function (e) { if (e.target === dom.ucffModal) dom.ucffModal.style.display = 'none'; });
        dom.ucffExportBtn.addEventListener('click', exportUcffAssessment);
        dom.ucffImportBtn.addEventListener('click', function () { dom.ucffFileInput.click(); });
        dom.ucffFileInput.addEventListener('change', importUcffAssessment);
        dom.ucffGrid.querySelector('thead').addEventListener('click', function (e) {
            var th = e.target.closest('th[data-sort]');
            if (th) sortUcffGrid(th.dataset.sort);
        });

        // Navigator exports
        document.getElementById('nav-export-svg').addEventListener('click', exportNavigatorSVG);
        document.getElementById('nav-export-json').addEventListener('click', exportNavigatorATTCKJSON);

        if (dom.baselinesSearchInput) {
            dom.baselinesSearchInput.addEventListener('input', debounce(function() {
                if (viewState === 'baselines') {
                    FlameData.loadBaselines().then(renderBaselinesGrid);
                }
            }, 200));
        }

        // Sidebar collapse/expand
        var collapseBtn = document.getElementById('sidebar-collapse-btn');
        var expandBtn = document.getElementById('sidebar-expand-btn');
        if (collapseBtn) {
            collapseBtn.addEventListener('click', function() {
                dom.filterPanel.classList.add('collapsed');
                if (expandBtn) expandBtn.style.display = 'block';
            });
        }
        if (expandBtn) {
            expandBtn.addEventListener('click', function() {
                dom.filterPanel.classList.remove('collapsed');
                expandBtn.style.display = 'none';
            });
        }

        // Collapsible filter groups (Fraud Types, Sectors)
        ['fraud-types-toggle', 'sectors-toggle'].forEach(function(toggleId) {
            var toggle = document.getElementById(toggleId);
            if (toggle) {
                toggle.addEventListener('click', function() {
                    toggle.classList.toggle('collapsed');
                    var wrapperId = toggleId.replace('-toggle', '') + '-wrapper';
                    // Map to correct wrapper ID
                    if (toggleId === 'fraud-types-toggle') wrapperId = 'filter-fraud-types-wrapper';
                    if (toggleId === 'sectors-toggle') wrapperId = 'filter-sectors-wrapper';
                    var wrapper = document.getElementById(wrapperId);
                    if (wrapper) wrapper.classList.toggle('collapsed');
                });
            }
        });

        // Search-within for sidebar filter sections
        ['filter-sectors-search', 'filter-fraud-types-search'].forEach(function(inputId) {
            var input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('input', function() {
                    var query = input.value.trim().toLowerCase();
                    var chipsContainer = input.parentElement.querySelector('.filter-chips');
                    if (!chipsContainer) return;
                    chipsContainer.querySelectorAll('.chip').forEach(function(chip) {
                        var text = (chip.textContent || '').toLowerCase();
                        chip.style.display = text.indexOf(query) !== -1 ? '' : 'none';
                    });
                });
            }
        });

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
        var hash = window.location.hash || '#browse';
        if (hash.startsWith('#detail/')) {
            showDetailView(hash.replace('#detail/', ''));
        } else if (hash === '#baselines') {
            showBaselinesView();
        } else {
            showBrowseView();
        }
        updateNavTabs(hash);
    }

    function navigateTo(target, id) {
        if (target === 'browse') {
            window.location.hash = '#browse';
        } else if (target === 'detail' && id) {
            window.location.hash = '#detail/' + id;
        } else if (target === 'baselines') {
            window.location.hash = '#baselines';
        }
    }

    function updateNavTabs(hash) {
        if (!dom.mainNav) return;
        dom.mainNav.querySelectorAll('.nav-tab').forEach(function(tab) {
            tab.classList.remove('active');
            var view = tab.getAttribute('data-view');
            if ((hash === '#browse' || hash.startsWith('#detail/')) && view === 'browse') tab.classList.add('active');
            else if (hash.startsWith('#baselines') && view === 'baselines') tab.classList.add('active');
        });
    }

    function hideAllViews() {
        dom.browseView.style.display = 'none';
        dom.detailView.style.display = 'none';
        if (dom.baselinesView) dom.baselinesView.style.display = 'none';
    }

    function showBrowseView() {
        viewState = 'browse';
        hideAllViews();
        dom.browseView.style.display = 'block';
        dom.filterPanel.classList.remove('detail-active');
    }

    function showDetailView(tpId) {
        viewState = 'detail';
        hideAllViews();
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

        if (browseMode === 'matrix') {
            renderMatrixView();
        }
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
    // Matrix View
    // -----------------------------------------------------------------------

    function initViewToggle() {
        if (!dom.viewMatrixBtn || !dom.viewGridBtn) return;

        dom.viewMatrixBtn.addEventListener('click', function () {
            setBrowseMode('matrix');
        });
        dom.viewGridBtn.addEventListener('click', function () {
            setBrowseMode('grid');
        });
    }

    function setBrowseMode(mode) {
        browseMode = mode;
        dom.viewMatrixBtn.classList.toggle('active', mode === 'matrix');
        dom.viewGridBtn.classList.toggle('active', mode === 'grid');
        dom.matrixView.style.display = mode === 'matrix' ? 'block' : 'none';
        dom.cardGrid.style.display = mode === 'grid' ? 'grid' : 'none';
        if (mode === 'matrix') {
            renderMatrixView();
        }
    }

    function getMatrixSectors() {
        var sectorCounts = {};
        filteredSubmissions.forEach(function (item) {
            (item.sectors || []).forEach(function (s) {
                sectorCounts[s] = (sectorCounts[s] || 0) + 1;
            });
        });
        return Object.keys(sectorCounts).sort(function (a, b) {
            return sectorCounts[b] - sectorCounts[a] || a.localeCompare(b);
        }).map(function (s) {
            return { key: s, count: sectorCounts[s] };
        });
    }

    function renderMatrixSectorTabs() {
        if (!dom.matrixSectorTabs) return;
        var sectors = getMatrixSectors();

        // NOTE: All values passed to escapeHtml() come from the FLAME index
        // JSON (authored data, not user input). The escapeHtml helper provides
        // defence-in-depth against any unexpected content.
        var html = '<button class="matrix-sector-tab' + (matrixSector === 'all' ? ' active' : '') + '" data-sector="all">All<span class="tab-count">' + escapeHtml(String(filteredSubmissions.length)) + '</span></button>';

        sectors.forEach(function (s) {
            html += '<button class="matrix-sector-tab' + (matrixSector === s.key ? ' active' : '') + '" data-sector="' + escapeHtml(s.key) + '">' + escapeHtml(formatLabel(s.key)) + '<span class="tab-count">' + escapeHtml(String(s.count)) + '</span></button>';
        });

        dom.matrixSectorTabs.innerHTML = html;

        dom.matrixSectorTabs.querySelectorAll('.matrix-sector-tab').forEach(function (tab) {
            tab.addEventListener('click', function () {
                matrixSector = tab.dataset.sector;
                renderMatrixView();
            });
        });
    }

    function renderMatrixView() {
        if (!dom.matrixTbody) return;

        renderMatrixSectorTabs();

        // Filter TPs by sector tab
        var tps = filteredSubmissions;
        if (matrixSector !== 'all') {
            tps = tps.filter(function (item) {
                return (item.sectors || []).indexOf(matrixSector) !== -1;
            });
        }

        dom.resultsBar.textContent = tps.length + ' of ' + allSubmissions.length + ' threat paths' + (matrixSector !== 'all' ? ' in ' + formatLabel(matrixSector) : '');

        // Build header — phase labels are static constants, safe to interpolate
        var thead = '<tr><th>Fraud Family</th>';
        PHASE_ORDER.forEach(function (phase) {
            thead += '<th class="phase-col" style="--phase-color: ' + PHASE_INFO[phase].color + '">' + escapeHtml(phase + ' ' + PHASE_INFO[phase].name) + '</th>';
        });
        thead += '</tr>';
        dom.matrixThead.innerHTML = thead;

        // Group TPs by fraud_family and primary_phase
        var matrix = {};
        FRAUD_FAMILY_ORDER.forEach(function (fam) {
            matrix[fam] = { P1: [], P2: [], P3: [], P4: [], P5: [], total: 0 };
        });

        var visibleIds = new Set();
        tps.forEach(function (item) { visibleIds.add(item.id); });

        filteredSubmissions.forEach(function (item) {
            var fam = item.fraud_family;
            var phase = item.primary_phase;
            if (!fam || !phase || !matrix[fam]) return;
            matrix[fam][phase].push(item);
            if (visibleIds.has(item.id)) {
                matrix[fam].total++;
            }
        });

        // Render rows — all interpolated values go through escapeHtml
        var tbody = '';
        FRAUD_FAMILY_ORDER.forEach(function (fam) {
            var row = matrix[fam];
            var label = FRAUD_FAMILY_LABELS[fam] || formatLabel(fam);
            var count = row.total;

            if (matrixSector !== 'all' && count === 0) return;

            tbody += '<tr>';
            tbody += '<td><div class="matrix-family-name">' + escapeHtml(label) + '</div>';
            tbody += '<div class="matrix-family-count">' + escapeHtml(String(count)) + ' threat path' + (count !== 1 ? 's' : '') + '</div></td>';

            PHASE_ORDER.forEach(function (phase) {
                tbody += '<td><div class="matrix-cell-chips">';
                row[phase].forEach(function (item) {
                    var dimmed = !visibleIds.has(item.id) ? ' dimmed' : '';
                    var chipLabel = item.short_name || item.id;
                    var chipTitle = item.id + ': ' + (item.title || '');
                    var confClass = '';
                    if (item.confidence_score != null) {
                        confClass = item.confidence_score >= 70 ? ' conf-high' : (item.confidence_score >= 40 ? ' conf-med' : ' conf-low');
                    }
                    tbody += '<a class="matrix-chip' + confClass + dimmed + '" href="#detail/' + escapeHtml(item.id) + '" title="' + escapeHtml(chipTitle) + '">' + escapeHtml(chipLabel) + '</a>';
                });
                tbody += '</div></td>';
            });

            tbody += '</tr>';
        });

        if (!tbody) {
            tbody = '<tr class="matrix-empty-row"><td colspan="6">No threat paths match the current filters.</td></tr>';
        }

        dom.matrixTbody.innerHTML = tbody;
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
        const f3 = item.mitre_f3 || [];
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

        // Export bar
        html += '<div class="detail-export-bar">';
        html += '<a href="api/v1/threat-paths/' + escapeHtml(item.id) + '.json" download class="export-btn">Export JSON</a>';
        html += '<button class="export-btn" id="export-stix-btn">Export STIX</button>';
        html += '</div>';

        // Attack flow diagram
        html += '<div class="attack-flow-section" id="attack-flow-section">';
        html += '<div class="attack-flow-container" id="attack-flow-container"></div>';
        html += '</div>';

        // Taxonomy toggle
        html += '<div class="taxonomy-toggle" id="taxonomy-toggle">';
        html += '<button class="tax-btn' + (activeTaxonomy === 'cfpf' ? ' active' : '') + '" data-taxonomy="cfpf">CFPF Phases</button>';
        html += '<button class="tax-btn' + (activeTaxonomy === 'mitre' ? ' active' : '') + '" data-taxonomy="mitre">MITRE ATT&CK</button>';
        html += '<button class="tax-btn' + (activeTaxonomy === 'f3' ? ' active' : '') + '" data-taxonomy="f3">MITRE F3</button>';
        html += '<button class="tax-btn' + (activeTaxonomy === 'groupib' ? ' active' : '') + '" data-taxonomy="groupib">Group-IB</button>';
        html += '</div>';

        // Phase timeline / taxonomy view
        if (activeTaxonomy === 'cfpf') {
            html += renderCfpfTimeline(phases);
        } else if (activeTaxonomy === 'mitre') {
            html += renderMitreView(mitre);
        } else if (activeTaxonomy === 'f3') {
            html += renderMitreF3View(f3);
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
        if (f3.length > 0 && activeTaxonomy !== 'f3') {
            html += '<div class="tag-group"><h4>MITRE F3</h4><div class="tag-list">';
            f3.forEach(function (t) { html += '<span class="detail-tag f3-tag">' + escapeHtml(t) + '</span>'; });
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

        // Ego neighborhood graph
        html += '<div class="ego-graph-section" id="ego-graph-section">';
        html += '<div class="ego-graph-header">';
        html += '<h3 class="ego-graph-title">Relationship Neighborhood</h3>';
        html += '<label class="ego-hop-toggle"><input type="checkbox" id="ego-2hop"> <span>2-hop</span></label>';
        html += '</div>';
        html += '<div class="ego-graph-container" id="ego-graph-container"></div>';
        html += '</div>';

        // Body content (rendered from markdown)
        if (item.body) {
            html += '<div class="detail-body" id="detail-body">';
            html += renderMarkdown(item.body);
            html += '</div>';
        }

        // Detection rules removed — see github.com/elchacal801/flame-detections

        dom.detailContent.innerHTML = html;

        // Post-render hooks
        bindTaxonomyToggle(item);
        addCopyButtons();
        highlightLookLeftRight();

        // Bind STIX export
        var stixBtn = document.getElementById('export-stix-btn');
        if (stixBtn) {
            stixBtn.addEventListener('click', function () { exportStix(item.id); });
        }

        // Render attack flow diagram
        if (item.body) {
            FlameViz.renderAttackFlow(
                document.getElementById('attack-flow-container'),
                item
            );
        }

        // Render ego neighborhood graph
        FlameViz.renderEgoGraph(
            document.getElementById('ego-graph-container'),
            item.id,
            { maxHops: 1, onNavigate: function (id) { navigateTo('detail', id); } }
        );
        var ego2hopCheckbox = document.getElementById('ego-2hop');
        if (ego2hopCheckbox) {
            ego2hopCheckbox.addEventListener('change', function () {
                FlameViz.renderEgoGraph(
                    document.getElementById('ego-graph-container'),
                    item.id,
                    { maxHops: this.checked ? 2 : 1, onNavigate: function (id) { navigateTo('detail', id); } }
                );
            });
        }

        // Scroll to top
        dom.detailView.scrollTop = 0;
        window.scrollTo(0, 0);
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

    function renderMitreF3View(techniques) {
        if (techniques.length === 0) {
            return '<div class="taxonomy-empty">No MITRE F3 mappings for this threat path.</div>';
        }
        let html = '<div class="mitre-grid">';
        techniques.forEach(function (t) {
            html += '<a class="mitre-card f3-card" href="https://ctid.mitre.org/fraud#/technique/' + encodeURIComponent(t) + '" target="_blank" rel="noopener">';
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

        var html = '';

        // Hero
        html += '<div class="about-hero">';
        html += '<span class="about-logo-icon">&#x1F525;</span>';
        html += '<span class="about-title">FLAME</span>';
        html += '<p class="about-tagline">Fraud Lifecycle Analysis &amp; Mitigation Exchange</p>';
        html += '</div>';

        // Live stats
        html += '<div class="about-stats-row">';
        html += '<div class="about-stat"><span class="about-stat-value">' + tp + '</span><span class="about-stat-label">Threat Paths</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">' + ft + '</span><span class="about-stat-label">Fraud Types</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">' + sec + '</span><span class="about-stat-label">Sectors</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">211</span><span class="about-stat-label">Detection Rules</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">14</span><span class="about-stat-label">Playbooks</span></div>';
        html += '<div class="about-stat"><span class="about-stat-value">6</span><span class="about-stat-label">Frameworks</span></div>';
        html += '</div>';

        // Overview
        html += '<div class="about-section">';
        html += '<p>FLAME is an open-source, community-driven platform for sharing structured fraud detection intelligence across organizational and framework boundaries. ';
        html += 'Every threat path maps simultaneously to <strong>6 fraud frameworks</strong>, exports to <strong>STIX 2.1 / MISP / TAXII / Sigma / CQL</strong>, and includes ';
        html += 'detection rules deployable to CrowdStrike NGSIEM, Splunk, Microsoft Sentinel, and Elasticsearch.</p>';
        html += '</div>';

        // Features grid — each card is clickable and expands inline
        html += '<h3>Platform Capabilities</h3>';
        html += '<p style="color:#888;font-size:13px;margin-top:-8px;">Click any capability to learn more.</p>';
        html += '<div class="about-features-grid">';

        var features = [
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                title: 'Threat Paths',
                desc: tp + ' structured fraud scheme analyses with CFPF lifecycle mapping',
                detail: 'Each threat path documents a complete fraud scheme across the 5-phase CFPF lifecycle (Recon, Initial Access, Positioning, Execution, Monetization). ' +
                    'Includes: threat hypothesis, confidence scoring (Admiralty Code), operational evidence, detection approaches with executable queries, controls & mitigations, ' +
                    'UCFF maturity alignment, and analyst notes. Browse via the <strong>Threat Paths</strong> tab or use the sidebar filters to narrow by sector, fraud type, or CFPF phase.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
                title: 'Detection Rules',
                desc: '211 Sigma-based rules exported to CQL, SPL, KQL, and EQL',
                detail: 'Each detection rule includes a Sigma-compatible detection block plus native query implementations for CrowdStrike CQL, Splunk SPL, Microsoft Sentinel KQL, and Elasticsearch EQL. ' +
                    'Rules are linked to specific threat paths and CFPF phases. Browse all rules via the <strong>Detection Rules</strong> tab, or view per-TP rules on any threat path detail page. ' +
                    'Export Sigma packs per threat path from the detail view export buttons.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
                title: 'MCP Server',
                desc: '7 AI-agent tools for conversational fraud intelligence',
                detail: 'The FLAME MCP server (Model Context Protocol) exposes 7 tools for LLM integration: <strong>search_threat_paths</strong>, <strong>get_threat_path</strong>, ' +
                    '<strong>get_detection_rules</strong>, <strong>map_framework</strong>, <strong>assess_coverage</strong>, <strong>get_baseline</strong>, and <strong>look_left_right</strong>. ' +
                    'Works with Claude Code, Cursor, and any MCP-compatible client. See <a href="https://github.com/elchacal801/flame-fraud/blob/main/docs/MCP-TOOLS.md" target="_blank">MCP-TOOLS.md</a> for full documentation.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
                title: 'STIX 2.1 / MISP / TAXII',
                desc: 'Full TIP integration with 4 custom fraud SDOs and subscribable feeds',
                detail: 'FLAME exports to three threat intelligence platform formats: <strong>STIX 2.1</strong> with 4 custom SDOs (x-flame-fraud-scheme, x-flame-financial-transaction, ' +
                    'x-flame-mule-network, x-flame-fraud-actor-profile), <strong>MISP</strong> galaxy with per-TP event feed, and <strong>TAXII 2.1</strong> static endpoints with 3 collections. ' +
                    'Download from the Resources section below or from the export buttons on each threat path detail page.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="5" cy="12" r="3"/><circle cx="19" cy="5" r="3"/><circle cx="19" cy="19" r="3"/><line x1="8" y1="12" x2="16" y2="5"/><line x1="8" y1="12" x2="16" y2="19"/></svg>',
                title: 'Relationship Graph',
                desc: 'Interactive D3.js visualization of cross-TP relationships',
                detail: 'The relationship graph visualizes typed connections between threat paths: <em>feeds-into</em>, <em>enables</em>, <em>shares-infrastructure</em>, ' +
                    '<em>provides-mules-for</em>, <em>escalates-from</em>, <em>variant-of</em>, and <em>related-to</em>. Click the graph icon in the header to open. ' +
                    'Nodes are color-coded by primary sector; hover to see connections. Also available: the <strong>Look Left / Look Right</strong> analysis on each TP detail page.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="3" x2="9" y2="21"/></svg>',
                title: 'Framework Navigator',
                desc: 'Cross-framework coverage matrix across CFPF, FT3, Group-IB, and ATT&CK',
                detail: 'The framework navigator shows a heat map of detection rule coverage across four frameworks simultaneously. Click the grid icon in the header to open. ' +
                    'Switch between CFPF, FT3, Group-IB Fraud Matrix, and MITRE ATT&CK tabs to see which techniques have detection rules and which are gaps. Export as SVG or ATT&CK Navigator JSON.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
                title: 'Coverage Assessment',
                desc: 'Organizational gap analysis by sector and fraud type',
                detail: 'Select your organization\'s sectors and fraud types to generate a coverage gap analysis. The tool shows which CFPF phases have detection coverage, ' +
                    'which fraud types lack threat paths, and recommends detection rules to deploy. Click the checkmark icon in the header to open. Results include a confidence-weighted coverage score.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
                title: 'Regulatory Pulse',
                desc: '6-source live feed (OFAC, FinCEN, SEC, OCC, FBI IC3, CFPB)',
                detail: 'The regulatory pulse is a live feed of fraud-relevant regulatory actions from 6 US sources, automatically fetched and mapped to threat paths by category. ' +
                    'Click the pulse icon (bottom-right corner) to view. Each alert shows source, date, severity, and linked threat paths. Feed refreshes via CI/CD automation.'
            },
            {
                icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
                title: 'Coverage Heat Map',
                desc: 'Fraud type vs CFPF phase detection density visualization',
                detail: 'The heat map shows a matrix of fraud types (rows) against CFPF phases (columns), colored by the number of threat paths covering each cell. ' +
                    'Darker cells indicate stronger detection coverage; lighter cells indicate gaps. Click the grid icon in the header to open.'
            }
        ];

        features.forEach(function (f, idx) {
            html += '<div class="about-feature-card about-feature-expandable" data-feature-idx="' + idx + '">';
            html += '<div class="about-feature-icon">' + f.icon + '</div>';
            html += '<div class="about-feature-title">' + f.title + ' <span class="about-feature-expand-arrow">&#9662;</span></div>';
            html += '<div class="about-feature-desc">' + f.desc + '</div>';
            html += '<div class="about-feature-detail" id="about-feature-detail-' + idx + '" style="display:none;">' + f.detail + '</div>';
            html += '</div>';
        });
        html += '</div>';

        // Supported frameworks
        html += '<h3>Supported Frameworks</h3>';
        html += '<div class="about-frameworks">';
        var frameworks = [
            { name: 'FS-ISAC CFPF', color: 'var(--color-p2)' },
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

        // Export formats
        html += '<h3>Export Formats</h3>';
        html += '<div class="about-frameworks">';
        ['STIX 2.1', 'MISP', 'TAXII 2.1', 'Sigma/SPL', 'Sigma/EQL', 'Sigma/KQL', 'CrowdStrike CQL', 'RSS 2.0', 'JSON API'].forEach(function(fmt) {
            html += '<span class="about-fw-badge" style="border-color: #555; color: #aaa;">' + fmt + '</span>';
        });
        html += '</div>';

        // Links
        html += '<h3>Resources &amp; Downloads</h3>';
        html += '<div class="about-links">';
        html += '<a href="https://github.com/elchacal801/flame-fraud" target="_blank" rel="noopener" class="about-link-btn">GitHub Repository</a>';
        html += '<a href="https://github.com/elchacal801/flame-fraud/blob/main/docs/ARCHITECTURE.md" target="_blank" rel="noopener" class="about-link-btn">Architecture Docs</a>';
        html += '<a href="https://github.com/elchacal801/flame-fraud/blob/main/docs/openapi.yaml" target="_blank" rel="noopener" class="about-link-btn">OpenAPI Spec</a>';
        html += '<a href="https://github.com/elchacal801/flame-fraud/blob/main/docs/MCP-TOOLS.md" target="_blank" rel="noopener" class="about-link-btn">MCP Tool Reference</a>';
        html += '<a href="api/v1/threat-paths.json" target="_blank" rel="noopener" class="about-link-btn">JSON API</a>';
        html += '<a href="api/taxii/discovery.json" target="_blank" rel="noopener" class="about-link-btn">TAXII Discovery</a>';
        html += '<a href="data/misp/flame-galaxy.json" target="_blank" rel="noopener" class="about-link-btn">MISP Galaxy</a>';
        html += '<a href="database/flame_stix_bundle.json" target="_blank" rel="noopener" class="about-link-btn">STIX Bundle</a>';
        html += '<a href="database/feed.xml" target="_blank" rel="noopener" class="about-link-btn">RSS Feed</a>';
        html += '<a href="https://github.com/elchacal801/flame-fraud/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener" class="about-link-btn">Contributing Guide</a>';
        html += '</div>';

        // License
        html += '<div class="about-license">';
        html += 'MIT License &middot; Open source &middot; TLP:WHITE &middot; Built by practitioners, for practitioners.';
        html += '</div>';

        dom.aboutBody.innerHTML = html;

        // Wire up feature card expand/collapse
        dom.aboutBody.querySelectorAll('.about-feature-expandable').forEach(function(card) {
            card.addEventListener('click', function() {
                var idx = card.getAttribute('data-feature-idx');
                var detail = document.getElementById('about-feature-detail-' + idx);
                if (!detail) return;
                var isOpen = detail.style.display !== 'none';
                // Close all others
                dom.aboutBody.querySelectorAll('.about-feature-detail').forEach(function(d) { d.style.display = 'none'; });
                dom.aboutBody.querySelectorAll('.about-feature-expandable').forEach(function(c) { c.classList.remove('about-feature-open'); });
                if (!isOpen) {
                    detail.style.display = 'block';
                    card.classList.add('about-feature-open');
                }
            });
        });
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
            if (a.mapped_tp_ids && a.mapped_tp_ids.length > 0) {
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

        // Robust date parser for heterogeneous regulatory date formats
        // Handles: ISO "2026-01-15", RFC 2822 "Wed, 14 Jan 2026",
        //          informal "Sept. 30, 2025", "Jan. 6, 2026", "Feb. 27, 2026",
        //          US slash "03/20/2025", publication "mm/dd/yyyy"
        var _MONTH_MAP = {
            jan: 0, january: 0, feb: 1, february: 1, mar: 2, march: 2,
            apr: 3, april: 3, may: 4, jun: 5, june: 5,
            jul: 6, july: 6, aug: 7, august: 7, sep: 8, sept: 8, september: 8,
            oct: 9, october: 9, nov: 10, november: 10, dec: 11, december: 11
        };

        function parseRegDate(str) {
            if (!str) return 0;
            // Try native Date.parse first (handles ISO, RFC 2822)
            var ts = Date.parse(str);
            if (!isNaN(ts)) return ts;
            // Handle informal: "Sept. 30, 2025", "Jan. 6, 2026"
            var m = str.match(/([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})/);
            if (m) {
                var mon = _MONTH_MAP[m[1].toLowerCase().replace(/\.$/, '')];
                if (mon !== undefined) return new Date(parseInt(m[3], 10), mon, parseInt(m[2], 10)).getTime();
            }
            // Handle "dd Mon yyyy" or "Mon dd, yyyy" other variants
            var m2 = str.match(/(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})/);
            if (m2) {
                var mon2 = _MONTH_MAP[m2[2].toLowerCase().replace(/\.$/, '')];
                if (mon2 !== undefined) return new Date(parseInt(m2[3], 10), mon2, parseInt(m2[1], 10)).getTime();
            }
            return 0;
        }

        // Sort alerts globally (descending date — newest first)
        var sortedAlerts = alerts.slice().sort(function (a, b) {
            return parseRegDate(b.date) - parseRegDate(a.date);
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
                var tpDisplay = (a.mapped_tp_ids && a.mapped_tp_ids.length > 0) ? a.mapped_tp_ids.length : '—';
                html += '<td style="text-align:center;">' + escapeHtml(String(tpDisplay)) + '</td>';
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
    // Relationship Graph — delegated to FlameViz (viz.js)
    // -----------------------------------------------------------------------

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
    // UCFF Maturity Self-Assessment
    // -----------------------------------------------------------------------

    var UCFF_DOMAINS = ['commit', 'assess', 'plan', 'act', 'monitor', 'report', 'improve'];

    var UCFF_LEVEL_DESCS = {
        1: 'Ad hoc, reactive fraud management',
        2: 'Basic fraud function with some defined processes',
        3: 'Formalized fraud program with proactive capabilities',
        4: 'Data-driven, continuously improving fraud program',
        5: 'Industry-leading, predictive fraud management',
    };

    var ucffUserLevels = {};
    var ucffResults = [];
    var ucffSortKey = 'gap';
    var ucffSortAsc = false;

    function initUcffAssessment() {
        var html = '<h3>Your Maturity Levels</h3>';
        UCFF_DOMAINS.forEach(function (d) {
            var level = ucffUserLevels[d] || 1;
            html += '<div class="ucff-domain-slider">';
            html += '<label>' + capitalize(d) + ' <span class="ucff-level-badge" id="ucff-badge-' + d + '">Level ' + level + '</span></label>';
            html += '<input type="range" min="1" max="5" value="' + level + '" id="ucff-slider-' + d + '" data-domain="' + d + '">';
            html += '<div class="ucff-level-desc" id="ucff-desc-' + d + '">' + UCFF_LEVEL_DESCS[level] + '</div>';
            html += '</div>';
        });
        dom.ucffSliderPanel.innerHTML = html;

        UCFF_DOMAINS.forEach(function (d) {
            if (!ucffUserLevels[d]) ucffUserLevels[d] = 1;
            document.getElementById('ucff-slider-' + d).addEventListener('input', function (e) {
                var val = parseInt(e.target.value);
                ucffUserLevels[d] = val;
                document.getElementById('ucff-badge-' + d).textContent = 'Level ' + val;
                document.getElementById('ucff-desc-' + d).textContent = UCFF_LEVEL_DESCS[val];
                computeUcffResults();
            });
        });

        computeUcffResults();
    }

    function parseUcffLevel(val) {
        if (!val || val === '') return 0;
        var m = String(val).match(/(\d)/);
        return m ? parseInt(m[1]) : 0;
    }

    function computeUcffResults() {
        var data = FlameData.getData();
        ucffResults = [];

        var ceilingLevels = {};
        UCFF_DOMAINS.forEach(function (d) { ceilingLevels[d] = 0; });

        data.forEach(function (tp) {
            var ucff = tp.ucff_domains || {};
            var gapScore = 0;
            var worstGap = 0;
            var worstDomain = '';

            UCFF_DOMAINS.forEach(function (d) {
                var required = parseUcffLevel(ucff[d]);
                if (required > ceilingLevels[d]) ceilingLevels[d] = required;
                var gap = Math.max(0, required - (ucffUserLevels[d] || 1));
                gapScore += gap;
                if (gap > worstGap) {
                    worstGap = gap;
                    worstDomain = d;
                }
            });

            var status = gapScore === 0 ? 'covered' : gapScore <= 3 ? 'partial' : 'blind';
            ucffResults.push({
                id: tp.id,
                title: tp.title,
                gap: gapScore,
                worst: worstDomain,
                worstGap: worstGap,
                status: status,
            });
        });

        var covered = ucffResults.filter(function (r) { return r.status === 'covered'; }).length;
        var partial = ucffResults.filter(function (r) { return r.status === 'partial'; }).length;
        var blind = ucffResults.filter(function (r) { return r.status === 'blind'; }).length;

        var domainGaps = {};
        UCFF_DOMAINS.forEach(function (d) { domainGaps[d] = 0; });
        ucffResults.forEach(function (r) {
            if (r.worst) domainGaps[r.worst] += r.worstGap;
        });
        var weakest = UCFF_DOMAINS.reduce(function (a, b) { return domainGaps[a] >= domainGaps[b] ? a : b; });

        dom.ucffSummary.innerHTML =
            '<div class="ucff-stat-card covered"><div class="ucff-stat-value">' + covered + '</div><div class="ucff-stat-label">Covered</div></div>' +
            '<div class="ucff-stat-card partial"><div class="ucff-stat-value">' + partial + '</div><div class="ucff-stat-label">Partial Gaps</div></div>' +
            '<div class="ucff-stat-card blind"><div class="ucff-stat-value">' + blind + '</div><div class="ucff-stat-label">Blind Spots</div></div>' +
            '<div class="ucff-stat-card"><div class="ucff-stat-value">' + capitalize(weakest) + '</div><div class="ucff-stat-label">Weakest Domain</div></div>';

        FlameViz.renderRadarChart(dom.ucffRadar, ucffUserLevels, ceilingLevels, UCFF_DOMAINS);

        sortUcffGrid(ucffSortKey, true);
    }

    function sortUcffGrid(key, skipToggle) {
        if (!skipToggle) {
            if (ucffSortKey === key) {
                ucffSortAsc = !ucffSortAsc;
            } else {
                ucffSortKey = key;
                ucffSortAsc = key === 'id' || key === 'title';
            }
        }

        dom.ucffGrid.querySelectorAll('th').forEach(function (th) {
            th.classList.remove('ucff-sort-active', 'ucff-sort-asc');
            if (th.dataset.sort === ucffSortKey) {
                th.classList.add('ucff-sort-active');
                if (ucffSortAsc) th.classList.add('ucff-sort-asc');
            }
        });

        var sorted = ucffResults.slice().sort(function (a, b) {
            var va = a[ucffSortKey], vb = b[ucffSortKey];
            if (typeof va === 'string') {
                var cmp = va.localeCompare(vb);
                return ucffSortAsc ? cmp : -cmp;
            }
            return ucffSortAsc ? va - vb : vb - va;
        });

        dom.ucffGridBody.innerHTML = sorted.map(function (r) {
            var statusClass = 'ucff-status-' + r.status;
            var statusLabel = r.status === 'covered' ? 'Covered' : r.status === 'partial' ? 'Partial' : 'Blind';
            return '<tr>' +
                '<td>' + escapeHtml(r.id) + '</td>' +
                '<td>' + escapeHtml(r.title) + '</td>' +
                '<td>' + r.gap + '</td>' +
                '<td>' + (r.worst ? capitalize(r.worst) : '\u2014') + '</td>' +
                '<td><span class="ucff-status ' + statusClass + '">' + statusLabel + '</span></td>' +
                '</tr>';
        }).join('');
    }

    function capitalize(s) {
        return s.charAt(0).toUpperCase() + s.slice(1);
    }

    function exportUcffAssessment() {
        var payload = {
            version: 1,
            timestamp: new Date().toISOString(),
            levels: Object.assign({}, ucffUserLevels),
        };
        var blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'flame-ucff-assessment.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    function importUcffAssessment(e) {
        var file = e.target.files[0];
        if (!file) return;
        var reader = new FileReader();
        reader.onload = function (ev) {
            try {
                var data = JSON.parse(ev.target.result);
                if (data.levels) {
                    UCFF_DOMAINS.forEach(function (d) {
                        if (data.levels[d] >= 1 && data.levels[d] <= 5) {
                            ucffUserLevels[d] = data.levels[d];
                        }
                    });
                    initUcffAssessment();
                }
            } catch (err) {
                alert('Invalid assessment file.');
            }
        };
        reader.readAsText(file);
        e.target.value = '';
    }

    // -----------------------------------------------------------------------
    // Baselines View
    // -----------------------------------------------------------------------

    var _baselineToTPs = null;

    function _buildBaselineToTPMap() {
        if (_baselineToTPs) return _baselineToTPs;
        _baselineToTPs = {};
        var tpData = FlameData.getData() || [];
        tpData.forEach(function(tp) {
            (tp.baseline_ids || []).forEach(function(blId) {
                if (!_baselineToTPs[blId]) _baselineToTPs[blId] = [];
                _baselineToTPs[blId].push(tp.id);
            });
        });
        return _baselineToTPs;
    }

    function showBaselinesView() {
        viewState = 'baselines';
        hideAllViews();
        dom.baselinesView.style.display = 'block';
        dom.filterPanel.classList.add('detail-active');

        FlameData.loadBaselines().then(function(baselines) {
            renderBaselinesGrid(baselines);
        });
    }

    function renderBaselinesGrid(baselines) {
        var query = (dom.baselinesSearchInput && dom.baselinesSearchInput.value || '').trim().toLowerCase();
        var filtered = baselines;
        if (query) {
            filtered = baselines.filter(function(b) {
                var haystack = ((b.id || '') + ' ' + (b.title || '') + ' ' + (b.description || '') + ' ' + (b.tags || []).join(' ')).toLowerCase();
                return haystack.indexOf(query) !== -1;
            });
        }

        if (filtered.length === 0) {
            dom.baselinesGrid.innerHTML = '<div class="empty-state">No baselines found.</div>';
            return;
        }

        var blToTP = _buildBaselineToTPMap();

        // NOTE: All values are escaped via escapeHtml before insertion — safe from XSS
        var html = '';
        filtered.forEach(function(b) {
            var linkedTPs = blToTP[b.id] || [];
            var tpCount = linkedTPs.length;
            html += '<div class="baseline-card" data-id="' + escapeHtml(b.id || '') + '">';
            html += '<div class="baseline-card-header">';
            html += '<span class="baseline-id">' + escapeHtml(b.id || '') + '</span>';
            html += '</div>';
            html += '<h3 class="baseline-card-title">' + escapeHtml(b.title || '') + '</h3>';
            if (b.description) {
                html += '<p class="baseline-card-desc">' + escapeHtml(truncate(b.description, 120)) + '</p>';
            }
            html += '<div class="baseline-card-meta">';
            if (b.tags && b.tags.length > 0) {
                b.tags.slice(0, 4).forEach(function(t) {
                    html += '<span class="baseline-tag">' + escapeHtml(t) + '</span>';
                });
                if (b.tags.length > 4) {
                    html += '<span class="baseline-tag more-tag">+' + (b.tags.length - 4) + '</span>';
                }
            }
            html += '</div>';
            if (linkedTPs.length > 0) {
                html += '<div class="baseline-linked-tps">';
                html += '<span class="baseline-tp-label">' + tpCount + ' Linked TP' + (tpCount !== 1 ? 's' : '') + ':</span> ';
                linkedTPs.forEach(function(tpId, i) {
                    html += '<a href="#detail/' + escapeHtml(tpId) + '" class="baseline-tp-link">' + escapeHtml(tpId) + '</a>';
                    if (i < linkedTPs.length - 1) html += ' ';
                });
                html += '</div>';
            } else {
                html += '<div class="baseline-linked-tps"><span class="baseline-tp-label">No linked TPs</span></div>';
            }
            html += '</div>';
        });
        dom.baselinesGrid.innerHTML = html;
    }

    // -----------------------------------------------------------------------
    // STIX Export
    // -----------------------------------------------------------------------

    function exportStix(tpId) {
        fetch('database/flame_stix_bundle.json')
            .then(function(response) {
                if (!response.ok) throw new Error('STIX bundle not available');
                return response.json();
            })
            .then(function(bundle) {
                var filtered = (bundle.objects || []).filter(function(obj) {
                    if (!obj.external_references) return false;
                    return obj.external_references.some(function(ref) {
                        return ref.external_id === tpId || (ref.source_name && ref.source_name.indexOf(tpId) !== -1);
                    });
                });

                var exportBundle = {
                    type: 'bundle',
                    id: 'bundle--' + tpId + '-export',
                    spec_version: bundle.spec_version || '2.1',
                    objects: filtered
                };

                var blob = new Blob([JSON.stringify(exportBundle, null, 2)], { type: 'application/json' });
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = tpId + '_stix_bundle.json';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            })
            .catch(function(err) {
                console.warn('STIX export failed:', err.message);
                alert('STIX bundle not available for export.');
            });
    }

    // -----------------------------------------------------------------------
    // Register Service Worker for PWA
    // -----------------------------------------------------------------------
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/service-worker.js')
                .then(function(reg) { console.log('SW registered:', reg.scope); })
                .catch(function(err) { console.log('SW registration failed:', err); });
        });
    }

    // -----------------------------------------------------------------------
    // End
    // -----------------------------------------------------------------------

})();
