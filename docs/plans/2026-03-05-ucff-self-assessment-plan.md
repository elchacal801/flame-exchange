# UCFF Maturity Self-Assessment Tool — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add an interactive UCFF maturity self-assessment widget to the FLAME frontend that compares user maturity levels against threat path requirements and visualizes coverage gaps.

**Architecture:** New header button opens a fullscreen modal with 7 maturity sliders (left panel) and live-updating results (right panel: D3 radar chart + sortable gap grid). All computation is client-side using `ucff_domains` data already present in `flame-index.json`. JSON save/load for assessment persistence.

**Tech Stack:** Vanilla JS, D3.js v7 (already loaded via CDN), existing FLAME CSS design system.

---

### Task 1: Add UCFF Modal Markup to index.html

**Files:**
- Modify: `index.html:87` (after contributors-btn, before header-actions div close)
- Modify: `index.html:~275` (after assess-modal closing div, before graph-modal)

**Step 1: Add header button**

Insert after the contributors-btn `</button>` (line 87), before the closing `</div>` of header-stats:

```html
                <button class="heat-map-btn" id="ucff-btn" title="UCFF Maturity Assessment">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                </button>
```

**Step 2: Add modal markup**

Insert after the assess-modal closing `</div>` (after line 275):

```html
    <!-- ================================================================ -->
    <!-- UCFF Maturity Assessment Modal                                   -->
    <!-- ================================================================ -->
    <div class="modal-overlay" id="ucff-modal" style="display:none;">
        <div class="modal-content modal-wide ucff-modal-content">
            <div class="modal-header">
                <h2>UCFF Maturity Self-Assessment</h2>
                <div class="ucff-header-actions">
                    <button class="ucff-action-btn" id="ucff-import-btn" title="Import Assessment">Import</button>
                    <button class="ucff-action-btn" id="ucff-export-btn" title="Export Assessment">Export</button>
                    <button class="modal-close" id="ucff-close">&times;</button>
                </div>
            </div>
            <div class="modal-body ucff-body">
                <div class="ucff-panels">
                    <!-- Left: Sliders -->
                    <div class="ucff-slider-panel" id="ucff-slider-panel"></div>
                    <!-- Right: Results -->
                    <div class="ucff-results-panel">
                        <div class="ucff-summary" id="ucff-summary"></div>
                        <div class="ucff-radar" id="ucff-radar"></div>
                        <div class="ucff-grid-wrapper">
                            <table class="ucff-grid" id="ucff-grid">
                                <thead>
                                    <tr>
                                        <th data-sort="id">TP ID</th>
                                        <th data-sort="title">Title</th>
                                        <th data-sort="gap" class="ucff-sort-active">Gap Score</th>
                                        <th data-sort="worst">Worst Gap</th>
                                        <th data-sort="status">Status</th>
                                    </tr>
                                </thead>
                                <tbody id="ucff-grid-body"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <input type="file" id="ucff-file-input" accept=".json" style="display:none;">
    </div>
```

**Step 3: Verify page loads**

Open `index.html` in browser — confirm new button appears in header, clicking it shows empty modal.

**Step 4: Commit**

```bash
git add index.html
git commit -m "feat(ucff): add modal markup and header button"
```

---

### Task 2: Add UCFF Modal Styles to style.css

**Files:**
- Modify: `style.css` (append at end before final closing comment)

**Step 1: Add styles**

Append to end of `style.css`:

```css
/* ================================================================ */
/* UCFF Maturity Assessment                                         */
/* ================================================================ */

.ucff-modal-content {
    max-width: 1100px;
    max-height: 90vh;
}

.ucff-body {
    padding: 0;
}

.ucff-panels {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 70vh;
}

.ucff-slider-panel {
    padding: var(--space-lg);
    border-right: 1px solid var(--color-border);
    overflow-y: auto;
}

.ucff-slider-panel h3 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-dim);
    margin-bottom: var(--space-lg);
}

.ucff-domain-slider {
    margin-bottom: var(--space-lg);
}

.ucff-domain-slider label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: var(--space-xs);
}

.ucff-domain-slider .ucff-level-badge {
    background: var(--color-accent);
    color: var(--color-bg);
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-weight: 700;
}

.ucff-domain-slider input[type="range"] {
    width: 100%;
    accent-color: var(--color-accent);
    cursor: pointer;
}

.ucff-domain-slider .ucff-level-desc {
    font-size: 0.72rem;
    color: var(--color-text-dim);
    margin-top: 2px;
    line-height: 1.3;
}

.ucff-results-panel {
    padding: var(--space-lg);
    overflow-y: auto;
    max-height: calc(90vh - 60px);
}

.ucff-summary {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}

.ucff-stat-card {
    background: var(--color-surface-2);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
}

.ucff-stat-card .ucff-stat-value {
    font-size: 1.5rem;
    font-weight: 700;
}

.ucff-stat-card .ucff-stat-label {
    font-size: 0.72rem;
    color: var(--color-text-dim);
    margin-top: 2px;
}

.ucff-stat-card.covered .ucff-stat-value { color: #22c55e; }
.ucff-stat-card.partial .ucff-stat-value { color: #eab308; }
.ucff-stat-card.blind .ucff-stat-value { color: #ef4444; }

.ucff-radar {
    margin-bottom: var(--space-lg);
    display: flex;
    justify-content: center;
}

.ucff-radar svg text {
    fill: var(--color-text);
    font-size: 11px;
}

.ucff-grid-wrapper {
    overflow-x: auto;
}

.ucff-grid {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
}

.ucff-grid th {
    text-align: left;
    padding: var(--space-sm) var(--space-md);
    border-bottom: 2px solid var(--color-border);
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    color: var(--color-text-dim);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.ucff-grid th:hover {
    color: var(--color-text);
}

.ucff-grid th.ucff-sort-active::after {
    content: ' \u25BC';
}

.ucff-grid th.ucff-sort-active.ucff-sort-asc::after {
    content: ' \u25B2';
}

.ucff-grid td {
    padding: var(--space-sm) var(--space-md);
    border-bottom: 1px solid var(--color-border);
}

.ucff-grid tbody tr:hover {
    background: var(--color-surface-2);
}

.ucff-grid .ucff-status {
    display: inline-block;
    padding: 2px 10px;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    font-weight: 600;
}

.ucff-status-covered { background: rgba(34,197,94,0.15); color: #22c55e; }
.ucff-status-partial { background: rgba(234,179,8,0.15); color: #eab308; }
.ucff-status-blind { background: rgba(239,68,68,0.15); color: #ef4444; }

.ucff-header-actions {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}

.ucff-action-btn {
    background: var(--color-surface-2);
    border: 1px solid var(--color-border);
    color: var(--color-text);
    padding: 4px 12px;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    cursor: pointer;
}

.ucff-action-btn:hover {
    background: var(--color-surface-3, var(--color-border));
}

@media (max-width: 768px) {
    .ucff-panels {
        grid-template-columns: 1fr;
    }
    .ucff-slider-panel {
        border-right: none;
        border-bottom: 1px solid var(--color-border);
    }
    .ucff-summary {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

**Step 2: Commit**

```bash
git add style.css
git commit -m "feat(ucff): add modal and component styles"
```

---

### Task 3: Add Radar Chart to viz.js

**Files:**
- Modify: `viz.js:978` (add `renderRadarChart` to returned public API)
- Modify: `viz.js:~975` (add function before the return statement)

**Step 1: Add renderRadarChart function**

Insert before the `return {` block (line 978):

```javascript
    // -------------------------------------------------------------------
    // UCFF Radar Chart
    // -------------------------------------------------------------------

    function renderRadarChart(container, userLevels, ceilingLevels, domains) {
        container.innerHTML = '';
        var size = 300, cx = size / 2, cy = size / 2, radius = 110;
        var n = domains.length;

        var svg = d3.select(container).append('svg')
            .attr('width', size).attr('height', size)
            .attr('viewBox', '0 0 ' + size + ' ' + size);

        // Draw grid rings (levels 1-5)
        for (var lvl = 1; lvl <= 5; lvl++) {
            var r = (lvl / 5) * radius;
            var ringPoints = domains.map(function (_, i) {
                var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
                return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
            });
            svg.append('polygon')
                .attr('points', ringPoints.map(function (p) { return p[0] + ',' + p[1]; }).join(' '))
                .attr('fill', 'none')
                .attr('stroke', 'var(--color-border)')
                .attr('stroke-width', lvl === 5 ? 1.5 : 0.5);
        }

        // Draw axis lines
        domains.forEach(function (_, i) {
            var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
            svg.append('line')
                .attr('x1', cx).attr('y1', cy)
                .attr('x2', cx + radius * Math.cos(angle))
                .attr('y2', cy + radius * Math.sin(angle))
                .attr('stroke', 'var(--color-border)')
                .attr('stroke-width', 0.5);
        });

        // Domain labels
        domains.forEach(function (d, i) {
            var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
            var lx = cx + (radius + 20) * Math.cos(angle);
            var ly = cy + (radius + 20) * Math.sin(angle);
            svg.append('text')
                .attr('x', lx).attr('y', ly)
                .attr('text-anchor', 'middle')
                .attr('dominant-baseline', 'middle')
                .style('font-size', '11px')
                .style('font-weight', '600')
                .style('text-transform', 'capitalize')
                .text(d);
        });

        function polyPoints(levels) {
            return domains.map(function (d, i) {
                var val = levels[d] || 0;
                var r = (val / 5) * radius;
                var angle = (Math.PI * 2 * i / n) - Math.PI / 2;
                return [cx + r * Math.cos(angle), cy + r * Math.sin(angle)];
            });
        }

        // Ceiling polygon (red)
        var ceilPts = polyPoints(ceilingLevels);
        svg.append('polygon')
            .attr('points', ceilPts.map(function (p) { return p[0] + ',' + p[1]; }).join(' '))
            .attr('fill', 'rgba(239,68,68,0.1)')
            .attr('stroke', '#ef4444')
            .attr('stroke-width', 2);

        // User polygon (blue)
        var userPts = polyPoints(userLevels);
        svg.append('polygon')
            .attr('points', userPts.map(function (p) { return p[0] + ',' + p[1]; }).join(' '))
            .attr('fill', 'rgba(59,130,246,0.15)')
            .attr('stroke', '#3b82f6')
            .attr('stroke-width', 2);

        // Legend
        var legend = svg.append('g').attr('transform', 'translate(8, ' + (size - 30) + ')');
        legend.append('rect').attr('width', 12).attr('height', 12).attr('fill', 'rgba(59,130,246,0.4)');
        legend.append('text').attr('x', 16).attr('y', 10).style('font-size', '10px').text('Your Maturity');
        legend.append('rect').attr('x', 110).attr('width', 12).attr('height', 12).attr('fill', 'rgba(239,68,68,0.4)');
        legend.append('text').attr('x', 126).attr('y', 10).style('font-size', '10px').text('Threat Ceiling');
    }
```

**Step 2: Add to public API**

Modify the return block to include the new function:

```javascript
    return {
        init: buildReverseRelationshipIndex,
        exportSVG: exportSVG,
        renderAttackFlow: renderAttackFlow,
        updateAttackFlowRules: updateAttackFlowRules,
        renderEgoGraph: renderEgoGraph,
        renderGlobalGraph: renderGlobalGraph,
        renderRadarChart: renderRadarChart,
        REL_COLORS: REL_COLORS,
        SECTOR_COLORS: SECTOR_COLORS,
    };
```

**Step 3: Commit**

```bash
git add viz.js
git commit -m "feat(ucff): add D3 radar chart to FlameViz"
```

---

### Task 4: Add UCFF Assessment Logic to app.js

**Files:**
- Modify: `app.js:52-95` (add DOM references in cacheDom)
- Modify: `app.js:~215` (add event listeners in bindEvents area)
- Modify: `app.js:~1825` (add UCFF functions before the closing `})();`)

**Step 1: Add DOM references**

Add these lines inside `cacheDom()` after the contributors lines (~line 94):

```javascript
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
```

**Step 2: Add event listeners**

Add after the contributors event listeners (find the pattern — after `contributorsBtn.addEventListener`):

```javascript
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
```

**Step 3: Add UCFF functions**

Insert before the closing `})();` (before line 1830):

```javascript
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
        // Build sliders
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

        // Initialize levels
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

        // Summary
        var covered = ucffResults.filter(function (r) { return r.status === 'covered'; }).length;
        var partial = ucffResults.filter(function (r) { return r.status === 'partial'; }).length;
        var blind = ucffResults.filter(function (r) { return r.status === 'blind'; }).length;

        // Weakest domain
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

        // Radar chart
        FlameViz.renderRadarChart(dom.ucffRadar, ucffUserLevels, ceilingLevels, UCFF_DOMAINS);

        // Grid
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

        // Update header classes
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
                '<td>' + (r.worst ? capitalize(r.worst) : '—') + '</td>' +
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
```

**Step 4: Verify in browser**

Open `index.html`, click the UCFF star button. Confirm:
- 7 sliders render with Level 1 defaults
- Radar chart shows blue polygon (small, all 1s) and red polygon (threat ceiling)
- Grid shows all 49 TPs sorted by gap score descending
- Moving sliders updates everything live
- Export downloads JSON, Import restores it

**Step 5: Commit**

```bash
git add app.js
git commit -m "feat(ucff): add assessment logic, scoring, save/load"
```

---

### Task 5: Final Integration Commit

**Step 1: Verify all files**

Confirm all 4 files are modified and the tool works end-to-end:
- `index.html` — button + modal markup
- `style.css` — UCFF component styles
- `viz.js` — radar chart function
- `app.js` — assessment logic, event handlers, save/load

**Step 2: Push**

```bash
git push origin main
```

**Step 3: Close issue**

```bash
gh issue close 11 --comment "Implemented UCFF maturity self-assessment tool. 7-domain slider input, D3 radar chart, sortable gap grid, JSON save/load."
```
