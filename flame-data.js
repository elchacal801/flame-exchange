/**
 * flame-data.js - FLAME Data Loader v2
 *
 * Loads flame-index.json on init (metadata-only, fast).
 * Lazy-loads individual TP content on demand.
 * Pre-computed stats from flame-stats.json.
 */

const FlameData = (function () {
    let _index = null;
    let _stats = null;
    let _contentCache = {};
    let _loading = false;
    let _callbacks = [];
    let _regulatoryAlerts = [];
    let _searchIndex = null;
    let _searchDocs = {};
    const INDEX_URL = 'database/flame-index.json';
    const STATS_URL = 'database/flame-stats.json';
    const CONTENT_BASE = 'database/flame-content/';
    const SEARCH_INDEX_URL = 'database/flame-search-index.json';

    /**
     * Load the index (metadata-only) and stats files.
     * Returns the index array.
     */
    async function load() {
        if (_index) return _index;
        if (_loading) {
            return new Promise(function (resolve, reject) {
                _callbacks.push({ resolve: resolve, reject: reject });
            });
        }

        _loading = true;

        try {
            var results = await Promise.all([
                fetch(INDEX_URL).then(function (r) {
                    if (!r.ok) throw new Error('Index load failed: ' + r.status);
                    return r.json();
                }),
                fetch(STATS_URL).then(function (r) {
                    if (!r.ok) throw new Error('Stats load failed: ' + r.status);
                    return r.json();
                })
            ]);

            _index = results[0];
            _stats = results[1];
            _loading = false;
            _callbacks.forEach(function (cb) { cb.resolve(_index); });
            _callbacks = [];
            return _index;
        } catch (err) {
            _loading = false;
            _callbacks.forEach(function (cb) { cb.reject(err); });
            _callbacks = [];
            throw err;
        }
    }

    /**
     * Get the index data (metadata-only array).
     */
    function getData() {
        return _index;
    }

    /**
     * Load full content for a single TP on demand.
     * Returns the full TP object including body markdown.
     */
    async function loadContent(tpId) {
        if (_contentCache[tpId]) return _contentCache[tpId];

        var response = await fetch(CONTENT_BASE + tpId + '.json');
        if (!response.ok) {
            throw new Error('Content load failed for ' + tpId + ': ' + response.status);
        }
        var data = await response.json();
        _contentCache[tpId] = data;
        return data;
    }

    /**
     * Extract unique values for a given field across all index entries.
     */
    function getUniqueValues(field) {
        if (!_index) return [];
        var values = new Set();
        _index.forEach(function (item) {
            var val = item[field];
            if (Array.isArray(val)) {
                val.forEach(function (v) { values.add(v); });
            } else if (val) {
                values.add(val);
            }
        });
        return Array.from(values).sort();
    }

    /**
     * Get pre-computed aggregate stats.
     */
    function getStats() {
        if (!_stats) return { total: 0, fraudTypes: 0, sectors: 0 };
        return _stats;
    }

    /**
     * Load regulatory alerts from regulatory-alerts.json.
     * Non-fatal: if the file is missing the panel simply stays hidden.
     */
    async function loadRegulatoryAlerts() {
        try {
            var response = await fetch('database/regulatory-alerts.json');
            if (!response.ok) throw new Error('Regulatory alerts load failed: ' + response.status);
            _regulatoryAlerts = await response.json();
        } catch (err) {
            console.warn('Regulatory alerts not available:', err.message);
            _regulatoryAlerts = [];
        }
        return _regulatoryAlerts;
    }

    /**
     * Get the loaded regulatory alerts array.
     */
    function getRegulatoryAlerts() {
        return _regulatoryAlerts;
    }

    /**
     * Load the search index and build a lunr.js index.
     * Non-fatal: falls back to substring search if unavailable.
     */
    async function loadSearchIndex() {
        if (_searchIndex) return _searchIndex;
        try {
            var response = await fetch(SEARCH_INDEX_URL);
            if (!response.ok) throw new Error('Search index load failed: ' + response.status);
            var docs = await response.json();

            docs.forEach(function (doc) {
                _searchDocs[doc.id] = doc;
            });

            _searchIndex = lunr(function () {
                this.ref('id');
                this.field('title', { boost: 10 });
                this.field('text');
                this.field('type');

                docs.forEach(function (doc) {
                    this.add(doc);
                }, this);
            });

            return _searchIndex;
        } catch (err) {
            console.warn('Search index not available, using fallback:', err.message);
            _searchIndex = null;
            return null;
        }
    }

    /**
     * Search using lunr.js index. Returns array of {id, score} or null if index unavailable.
     */
    function search(query) {
        if (!_searchIndex || !query) return null;
        try {
            return _searchIndex.search(query);
        } catch (e) {
            // lunr parse error on special chars — try wildcard
            try {
                return _searchIndex.search(query.replace(/[^a-zA-Z0-9 ]/g, '') + '*');
            } catch (e2) {
                return null;
            }
        }
    }

    /**
     * Load baselines data.
     */
    var _baselines = null;
    async function loadBaselines() {
        if (!_baselines) {
            try {
                var response = await fetch('api/v1/baselines.json');
                if (!response.ok) throw new Error('Baselines load failed: ' + response.status);
                var result = await response.json();
                _baselines = result.data || result;
            } catch (err) {
                console.warn('Baselines not available:', err.message);
                _baselines = [];
            }
        }
        return _baselines;
    }

    return {
        load: load,
        getData: getData,
        loadContent: loadContent,
        getUniqueValues: getUniqueValues,
        getStats: getStats,
        loadRegulatoryAlerts: loadRegulatoryAlerts,
        getRegulatoryAlerts: getRegulatoryAlerts,
        loadSearchIndex: loadSearchIndex,
        search: search,
        loadBaselines: loadBaselines,
    };
})();
