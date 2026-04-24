

class ChemicalElement {
    constructor(data, index) {
        this.num = data[0];
        this.sym = data[1];
        this.name = data[2];
        this.col = data[3];
        this.row = data[4];
        this.catId = data[5];
        this.catName = catNames[this.catId];
        this.en = data[6];
        this.ep = (this.en > 0) ? (4.0 - this.en) : 0;
        if (this.catId === 8 && this.en === 0) this.ep = 0;
        
        this.yearStr = discYears[index];
        this.yearNum = this.yearStr === "Ancient" ? 0 : parseInt(this.yearStr);
        this.mass = data[7];
        this.state = data[8];
        
        let fullConfig = data[9];
        for (let core in nobleCores) {
            if (fullConfig.startsWith(core)) {
                fullConfig = fullConfig.replace(core, nobleCores[core]);
                break;
            }
        }
        this.config = fullConfig;
        this.oxidation = improvedOxidationData[this.sym] || data[10];
        this.exception = data[11];

        const extra = extraData[this.num] || { mp: 'Unknown', bp: 'Unknown', use: 'Unknown' };
        this.mp = extra.mp;
        this.bp = extra.bp;
        this.use = extra.use;
    }

    getStateColor() { return stateColors[this.state] || "#000000"; }
    getCategoryColor() { return catColors[this.catId]; }
}

class PeriodicTableUI {
    constructor(elements, appController) {
        this.elements = elements;
        this.appController = appController;
        this.tableEl = document.getElementById('table');
        this.periodLabelsEl = document.getElementById('period-labels');
        this.groupLabelsEl = document.getElementById('group-labels');
        this.lanthanidesEl = document.getElementById('lanthanides');
        this.actinidesEl = document.getElementById('actinides');
        
        this.renderLabels();
        this.renderGrid();
    }

    renderLabels() {
        this.periodLabelsEl.innerHTML = '';
        for (let i = 1; i <= 7; i++) {
            const div = document.createElement('div');
            div.className = 'period-label'; div.textContent = i;
            this.periodLabelsEl.appendChild(div);
        }
        this.groupLabelsEl.innerHTML = '';
        for (let i = 1; i <= 18; i++) {
            const div = document.createElement('div');
            div.className = 'group-label'; div.textContent = i;
            this.groupLabelsEl.appendChild(div);
        }
    }

    renderGrid() {
        this.tableEl.innerHTML = '';
        this.lanthanidesEl.innerHTML = '';
        this.actinidesEl.innerHTML = '';

        this.elements.forEach(el => {
            const div = this.createElementCard(el);
            if (el.catId === 9) this.lanthanidesEl.appendChild(div);
            else if (el.catId === 10) this.actinidesEl.appendChild(div);
            else this.tableEl.appendChild(div);
        });
    }

    createElementCard(el) {
        const div = document.createElement('div');
        div.className = 'element';
        div.id = `el-${el.num}`;
        div.style.setProperty('--state-color', el.getStateColor());
        if (el.catId !== 9 && el.catId !== 10) {
            div.style.gridColumn = el.col;
            div.style.gridRow = el.row;
        }

        div.innerHTML = `
            <div class="element-content">
                <span class="atomic-number">${el.num}</span>
                <span class="symbol" style="color: ${el.getStateColor()}">${el.sym}</span>
                <span class="element-name">${el.name}</span>
                <span class="dynamic-value" id="val-${el.num}">${el.mass}</span>
                <span class="state-indicator">${stateNames[el.state]}</span>
            </div>
        `;

        div.addEventListener('mouseenter', () => this.appController.handleHover(el));
        div.addEventListener('mouseleave', () => this.appController.handleHoverOut(el));
        div.addEventListener('click', () => this.appController.handleClick(el, div));

        this.applyViewColor(div, el, this.appController.currentView);
        return div;
    }

    getHeatmapColor(value, min, max, colorStart, colorEnd) {
        if (value === 0 || value === "N/A") return colorStart;
        let ratio = (value - min) / (max - min);
        if (ratio < 0) ratio = 0;
        if (ratio > 1) ratio = 1;
        return `color-mix(in srgb, ${colorEnd} ${ratio * 100}%, ${colorStart})`;
    }

    applyViewColor(div, el, view) {
        if (view === 'category' || view === 'detail') {
            div.style.backgroundColor = el.getCategoryColor();
        } else if (view === 'en') {
            div.style.backgroundColor = this.getHeatmapColor(el.en, 0, 4.0, '#1a1d24', '#ef4444');
        } else if (view === 'ep') {
            div.style.backgroundColor = this.getHeatmapColor(el.ep, 0, 3.3, '#1a1d24', '#3b82f6');
        } else if (view === 'discovered') {
            div.style.backgroundColor = el.yearNum === 0 ? '#1e293b' : this.getHeatmapColor(el.yearNum, 1700, 2020, '#1a1d24', '#f59e0b');
        }
    }

    updateView(view) {
        this.elements.forEach(el => {
            const div = document.getElementById(`el-${el.num}`);
            if (div) {
                this.applyViewColor(div, el, view);
                const valSpan = div.querySelector(`#val-${el.num}`);
                if (view === 'en') valSpan.textContent = el.en > 0 ? el.en : 'N/A';
                else if (view === 'ep') valSpan.textContent = el.ep > 0 ? el.ep : 'N/A';
                else if (view === 'discovered') valSpan.textContent = el.yearStr;
                else valSpan.textContent = el.mass;
            }
        });
    }

    updateLegend(view) {
        const legend = document.getElementById('legend');
        if (view === 'category' || view === 'detail') {
            let html = '<strong style="width: 100%; text-align: center; color: var(--accent); margin-bottom: 10px;">Element Classification:</strong>';
            Object.entries(catColors).forEach(([id, color]) => {
                html += `<div class="legend-item"><div class="legend-color" style="background-color: ${color}"></div> <span>${catNames[id]}</span></div>`;
            });
            legend.innerHTML = html;
        } else {
            let color = view === 'en' ? '#ef4444' : view === 'ep' ? '#3b82f6' : '#f59e0b';
            let labelLow = view === 'discovered' ? 'Ancient' : 'Low';
            let labelHigh = view === 'discovered' ? 'Modern' : 'High';
            legend.innerHTML = `
                <div style="width: 100%; display: flex; align-items: center; gap: 10px;">
                    <span>${labelLow}</span>
                    <div class="gradient-bar" style="background: linear-gradient(to right, #1a1d24, ${color})"></div>
                    <span>${labelHigh}</span>
                </div>
            `;
        }
    }

    clearSelections() {
        document.querySelectorAll('.element').forEach(el => {
            el.classList.remove('selected', 'locked', 'reacting');
        });
    }
}

class DashboardUI {
    constructor() {
        this.infoPanel = document.getElementById('info-panel');
        this.comparePanel = document.getElementById('compare-panel');
        this.reactionPanel = document.getElementById('reaction-panel');
        this.infoContent = document.getElementById('info-content');
        this.compareContent = document.getElementById('compare-content');
        this.reactionContent = document.getElementById('reaction-content');
    }

    setMode(mode) {
        this.infoPanel.style.display = mode === 'info' ? 'block' : 'none';
        this.comparePanel.style.display = mode === 'compare' ? 'block' : 'none';
        this.reactionPanel.style.display = mode === 'reaction' ? 'block' : 'none';
    }

    resetInfo() {
        this.infoContent.innerHTML = `<p style="color: #9ca3af; font-size: 13px;">💡 <strong>Hover over an element</strong> to preview, or <strong>click an element</strong> to lock its properties here.</p>`;
    }

    renderInfo(el, isLocked) {
        const exceptionNote = el.exception ? `<div class="stat-row"><span class="stat-label">⚠️ Exception:</span> <span class="stat-value" style="color: #fbbf24;"><strong>Has exception to Aufbau principle</strong></span></div>` : '';
        const lockNotice = isLocked ? `<div style="text-align:center; color:#f59e0b; font-size:12px; margin-bottom:10px;">🔒 Locked View (Click again to unlock)</div>` : '';

        this.infoContent.innerHTML = `
            ${lockNotice}
            <div class="element-detail">
                <div class="stat-row"><span class="stat-label">Element:</span> <span class="stat-value">${el.name} (${el.sym})</span></div>
            </div>
            <div class="stat-row"><span class="stat-label">Atomic Number:</span> <span class="stat-value"><strong>${el.num}</strong></span></div>
            <div class="stat-row"><span class="stat-label">Atomic Mass:</span> <span class="stat-value">${el.mass} u</span></div>
            <div class="stat-row"><span class="stat-label">Classification:</span> <span class="stat-value" style="color:${el.getCategoryColor()}"><strong>${el.catName}</strong></span></div>
            <div class="stat-row"><span class="stat-label">State of Matter:</span> <span class="stat-value" style="color: ${el.getStateColor()}; text-shadow: 0 0 5px ${el.getStateColor()};"><strong>${stateNames[el.state]}</strong></span></div>
            <div class="stat-row"><span class="stat-label">Electron Config:</span> <span class="stat-value" style="font-family: monospace;">${el.config}</span></div>
            ${exceptionNote}
            <div class="stat-row"><span class="stat-label">Oxidation States:</span> <span class="stat-value">${el.oxidation}</span></div>
            <div class="stat-row"><span class="stat-label">Electronegativity:</span> <span class="stat-value">${el.en > 0 ? el.en : 'N/A'}</span></div>
            <div class="stat-row"><span class="stat-label">Electropositivity:</span> <span class="stat-value">${el.ep > 0 ? el.ep : 'N/A'}</span></div>
            <div class="stat-row"><span class="stat-label">Year Discovered:</span> <span class="stat-value">${el.yearStr}</span></div>
            <div class="stat-row"><span class="stat-label">Melting Point:</span> <span class="stat-value">${el.mp !== 'Unknown' ? el.mp + ' °C' : 'Unknown'}</span></div>
            <div class="stat-row"><span class="stat-label">Boiling Point:</span> <span class="stat-value">${el.bp !== 'Unknown' ? el.bp + ' °C' : 'Unknown'}</span></div>
            <div class="stat-row"><span class="stat-label">Common Uses:</span> <span class="stat-value">${el.use}</span></div>
            <div style="margin-top: 20px; text-align: center;">
                <a href="https://www.google.com/search?tbm=isch&q=${encodeURIComponent(el.name)}+element" target="_blank" style="display: inline-block; padding: 8px 12px; background-color: var(--accent); color: white; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; transition: background-color 0.2s;">🖼️ View Images on Google</a>
            </div>
        `;
    }

    renderCompare(compareSelection) {
        if (compareSelection.length === 0) {
            this.compareContent.innerHTML = "Select two elements from the table to compare."; return;
        }
        if (compareSelection.length === 1) {
            this.compareContent.innerHTML = `Selected <strong style="color: var(--compare-active)">${compareSelection[0].name}</strong>. Select one more from the table.`; return;
        }

        const e1 = compareSelection[0]; const e2 = compareSelection[1];
        const enWinner = e1.en > e2.en ? e1 : (e2.en > e1.en ? e2 : null);
        const epWinner = e1.ep > e2.ep ? e1 : (e2.ep > e1.ep ? e2 : null);

        const formatStat = (stat1, stat2, winner) => {
            const s1 = winner === e1 ? `<span class="compare-winner">${stat1}</span>` : stat1;
            const s2 = winner === e2 ? `<span class="compare-winner">${stat2}</span>` : stat2;
            return `${s1} vs ${s2}`;
        };

        this.compareContent.innerHTML = `
            <div style="display:flex; justify-content:space-between; margin-bottom:15px; gap: 10px;">
                <strong style="color:${e1.getCategoryColor()}; font-size:18px;">${e1.sym}</strong>
                <span style="color: #9ca3af;">VS</span>
                <strong style="color:${e2.getCategoryColor()}; font-size:18px;">${e2.sym}</strong>
            </div>
            <div class="stat-row"><span class="stat-label">Element Names:</span> <span class="stat-value">${e1.name} vs ${e2.name}</span></div>
            <div class="stat-row"><span class="stat-label">Atomic Numbers:</span> <span class="stat-value">${e1.num} vs ${e2.num}</span></div>
            <div class="stat-row"><span class="stat-label">Atomic Masses:</span> <span class="stat-value">${e1.mass} vs ${e2.mass}</span></div>
            <div class="stat-row"><span class="stat-label">Classification:</span> <span class="stat-value">${e1.catName} vs ${e2.catName}</span></div>
            <div class="stat-row"><span class="stat-label">States:</span> <span class="stat-value"><span style="color: ${e1.getStateColor()}; text-shadow: 0 0 5px ${e1.getStateColor()}; font-weight: bold;">${stateNames[e1.state]}</span> <span style="color: #9ca3af;">vs</span> <span style="color: ${e2.getStateColor()}; text-shadow: 0 0 5px ${e2.getStateColor()}; font-weight: bold;">${stateNames[e2.state]}</span></span></div>
            <div class="stat-row"><span class="stat-label">Electronegativity:</span> <span>${formatStat(e1.en||'N/A', e2.en||'N/A', enWinner)}</span></div>
            <div class="stat-row"><span class="stat-label">Electropositivity:</span> <span>${formatStat(e1.ep||'N/A', e2.ep||'N/A', epWinner)}</span></div>
            <div class="stat-row"><span class="stat-label">Oxidation States:</span> <span class="stat-value">${e1.oxidation} vs ${e2.oxidation}</span></div>
            <div class="stat-row"><span class="stat-label">Discovered:</span> <span class="stat-value">${e1.yearStr} vs ${e2.yearStr}</span></div>
            <div class="stat-row"><span class="stat-label">Melting Point:</span> <span class="stat-value">${e1.mp}°C vs ${e2.mp}°C</span></div>
            <div class="stat-row"><span class="stat-label">Boiling Point:</span> <span class="stat-value">${e1.bp}°C vs ${e2.bp}°C</span></div>
            <div class="stat-row"><span class="stat-label">Common Uses:</span> <span class="stat-value" style="font-size: 11px;">${e1.use} <br><span style="color:#9ca3af;">vs</span><br> ${e2.use}</span></div>
        `;
    }

    renderReactionSetup(reactionSelection, reactionType, appController) {
        let title = "Reaction Simulator";
        let instruction = "";

        if (reactionType === 'combination') {
            title = "Combination Reaction (Cross-Multiply)";
            instruction = reactionSelection.length === 0 ? "Select 1st element from the table (Metal/Cation)." : (reactionSelection.length === 1 ? `Selected <strong style="color: var(--reaction-active)">${reactionSelection[0].name}</strong>. Select 2nd element (Nonmetal/Anion).` : "Calculating...");
        } else if (reactionType === 'displacement') {
            title = "Single Displacement Reaction";
            instruction = reactionSelection.length === 0 ? "Select a Metal from the table to displace the compound." : "Calculating...";
        } else if (reactionType === 'decomposition') {
            title = "Decomposition Reaction";
            instruction = "Select a compound to decompose.";
        } else if (reactionType === 'acidbase') {
            title = "Acid-Base Reaction";
            instruction = reactionSelection.length === 0 ? "Select a Metal (Base) or Nonmetal (Acid) to react with water/acid." : "Calculating...";
        }

        let selectHtml = `
            <select id="reaction-type-select" class="reaction-dropdown">
                <option value="combination" ${reactionType==='combination'?'selected':''}>Combination (A + B → AB)</option>
                <option value="decomposition" ${reactionType==='decomposition'?'selected':''}>Decomposition (AB → A + B)</option>
                <option value="displacement" ${reactionType==='displacement'?'selected':''}>Single Displacement (A + BC → AC + B)</option>
                <option value="acidbase" ${reactionType==='acidbase'?'selected':''}>Acid-Base (Neutralization)</option>
            </select>
        `;

        let extraDropdown = '';
        
        const getOptions = (typeMatch) => {
            let options = '';
            for (let [formula, comp] of Object.entries(compoundDatabase)) {
                if (comp.rTypes && comp.rTypes.toLowerCase().includes(typeMatch)) {
                    options += `<option value="${formula}">${comp.name} (${formula})</option>`;
                }
            }
            return options;
        };

        if (reactionType === 'displacement') {
            extraDropdown = `<select id="compound-select" class="reaction-dropdown">${getOptions('displacement')}</select>`;
        } else if (reactionType === 'decomposition') {
             extraDropdown = `<select id="compound-select" class="reaction-dropdown">${getOptions('decomposition')}</select>`;
        }

        this.reactionContent.innerHTML = `
            ${selectHtml}
            ${extraDropdown}
            <p style="color: #9ca3af; font-size: 13px;">💡 ${instruction}</p>
        `;

        document.getElementById('reaction-type-select').addEventListener('change', (e) => {
            appController.setReactionType(e.target.value);
        });
        
        const compoundSelect = document.getElementById('compound-select');
        if (compoundSelect) {
            compoundSelect.addEventListener('change', (e) => {
                appController.setReactionCompound(e.target.value);
            });
            // Auto trigger for decomposition
            if (reactionType === 'decomposition') appController.runReaction();
        }
    }

    renderReactionResult(resultHtml) {
        // Appends the result below the setup
        const resultDiv = document.createElement('div');
        resultDiv.innerHTML = resultHtml;
        this.reactionContent.appendChild(resultDiv);
    }
}

class ReactionEngine {
    constructor() {}

    predictCombination(el1, el2) {
        if (!el1.oxidation || !el2.oxidation) return { error: "Missing oxidation state data." };

        const parseOxis = (str) => str.split(',').map(s => parseInt(s.trim()));
        const oxis1 = parseOxis(el1.oxidation);
        const oxis2 = parseOxis(el2.oxidation);

        // Find a positive and a negative
        let cation = null, anion = null, vCat = 0, vAn = 0;

        // Try el1 as cation, el2 as anion
        let pos1 = oxis1.find(v => v > 0);
        let neg2 = oxis2.find(v => v < 0);

        if (pos1 !== undefined && neg2 !== undefined) {
            cation = el1; anion = el2; vCat = pos1; vAn = Math.abs(neg2);
        } else {
            // Try el2 as cation, el1 as anion
            let pos2 = oxis2.find(v => v > 0);
            let neg1 = oxis1.find(v => v < 0);
            if (pos2 !== undefined && neg1 !== undefined) {
                cation = el2; anion = el1; vCat = pos2; vAn = Math.abs(neg1);
            }
        }

        if (!cation || !anion) {
            return { error: "These elements do not have compatible oxidation states for a simple ionic combination." };
        }

        const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
        let divisor = gcd(vCat, vAn);
        let rCat = vAn / divisor;
        let rAn = vCat / divisor;

        let formula = `${cation.sym}${rCat > 1 ? `<sub>${rCat}</sub>` : ''}${anion.sym}${rAn > 1 ? `<sub>${rAn}</sub>` : ''}`;
        return {
            equation: `${cation.sym} + ${anion.sym} → ${formula}`,
            desc: `${cation.name} (+${vCat}) reacts with ${anion.name} (-${vAn}) to form ${formula}.`
        };
    }

    checkDisplacement(metal, compoundId) {
        if (!reactivitySeries.includes(metal.sym)) {
            return { error: `${metal.name} is not in the simplified reactivity series for this simulation.` };
        }
        
        const comp = compoundDatabase[compoundId];
        if (!comp) return { error: "Unknown compound" };

        let targetIon = comp.cation;
        if (!targetIon) return { error: "Compound has no defined cation for displacement." };

        if (!reactivitySeries.includes(targetIon)) {
            return { error: `Compound cation (${targetIon}) not in reactivity series.` };
        }

        const metalIndex = reactivitySeries.indexOf(metal.sym);
        const targetIndex = reactivitySeries.indexOf(targetIon);

        if (metalIndex < targetIndex) {
            // Metal is more reactive, displacement occurs
            let vMetal = Math.abs(parseInt(metal.oxidation.split(',').pop() || "2"));
            if (isNaN(vMetal) || vMetal === 0) vMetal = 2; // fallback

            let targetValency = comp.valCat;
            let anionValency = comp.valAn;
            let anionSym = comp.anion;

            // New compound: metal + anion
            const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
            let div = gcd(vMetal, anionValency);
            let rMetal = anionValency / div;
            let rAnion = vMetal / div;

            let newComp = `${metal.sym}${rMetal > 1 ? `<sub>${rMetal}</sub>` : ''}${anionSym}${rAnion > 1 ? `<sub>${rAnion}</sub>` : ''}`;
            
            return {
                equation: `${metal.sym} + ${compoundId} → ${newComp} + ${targetIon}`,
                desc: `${metal.name} is more reactive than ${targetIon} and displaces it from ${comp.name}.`
            };
        } else {
            return {
                equation: `${metal.sym} + ${compoundId} → No Reaction`,
                desc: `${metal.name} is less reactive than ${targetIon}.`
            };
        }
    }

    getDecomposition(compoundId) {
        const comp = compoundDatabase[compoundId];
        if (!comp) return { error: "Unknown compound." };

        // Some hardcoded generic equations based on the user's dataset hints
        if (compoundId === "H2O") return { equation: "2H<sub>2</sub>O → 2H<sub>2</sub> + O<sub>2</sub>", desc: "Electrolysis of water." };
        if (compoundId === "CaCO3") return { equation: "CaCO<sub>3</sub> → CaO + CO<sub>2</sub>", desc: "Thermal decomposition." };
        if (compoundId === "NaCl") return { equation: "2NaCl → 2Na + Cl<sub>2</sub>", desc: "Electrolysis of molten salt." };
        if (compoundId === "KClO3") return { equation: "2KClO<sub>3</sub> → 2KCl + 3O<sub>2</sub>", desc: "Thermal decomposition (Yields O2 gas)." };
        if (compoundId === "H2O2") return { equation: "2H<sub>2</sub>O<sub>2</sub> → 2H<sub>2</sub>O + O<sub>2</sub>", desc: "Decomposition (Yields H2O+O2)." };
        if (compoundId === "KNO3") return { equation: "2KNO<sub>3</sub> → 2KNO<sub>2</sub> + O<sub>2</sub>", desc: "Decomposition (Yields O2 and KNO2)." };
        if (compoundId === "NaHCO3") return { equation: "2NaHCO<sub>3</sub> → Na<sub>2</sub>CO<sub>3</sub> + H<sub>2</sub>O + CO<sub>2</sub>", desc: "Thermal decomposition (Heating)." };
        if (comp.anion === "SO4") return { equation: `${compoundId} → Metal Oxide + SO<sub>3</sub>`, desc: "Thermal decomposition of a sulfate." };
        
        return { error: `Specific decomposition equation for ${comp.name} not programmed.` };
    }

    getAcidBase(el) {
        if (el.catId === 1 || el.catId === 2) {
            return {
                equation: `${el.sym} + H<sub>2</sub>O → ${el.sym}OH + H<sub>2</sub>`,
                desc: `Active metals react with water to form basic hydroxides.`
            };
        } else if (el.catId === 6 || el.catId === 7) {
            return {
                equation: `${el.sym}O<sub>x</sub> + H<sub>2</sub>O → H<sub>y</sub>${el.sym}O<sub>z</sub>`,
                desc: `Nonmetal oxides react with water to form acidic solutions.`
            };
        } else {
            return { error: "This element does not have a simple binary acid/base reaction simulated." };
        }
    }
}

class AppController {
    constructor() {
        this.elements = rawData.map((d, i) => new ChemicalElement(d, i));
        this.currentView = 'category';
        this.mode = 'info'; // info, compare, reaction
        this.lockedElement = null;
        this.compareSelection = [];
        this.reactionSelection = [];
        this.reactionType = 'combination';
        this.reactionCompound = 'HCl';

        this.dashboardUI = new DashboardUI();
        this.ui = new PeriodicTableUI(this.elements, this);
        this.reactionEngine = new ReactionEngine();

        this.setupButtons();
        this.setupSearch();
        this.ui.updateLegend(this.currentView);
    }

    setupButtons() {
        ['category', 'en', 'ep', 'discovered', 'detail'].forEach(view => {
            document.getElementById(`btn-${view==='category'?'cat':(view==='discovered'?'disc':view)}`).addEventListener('click', (e) => {
                this.currentView = view;
                document.querySelectorAll('.header-controls button:not(.compare-mode):not(.reaction-mode)').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.ui.updateView(view);
                this.ui.updateLegend(view);
            });
        });

        const btnCompare = document.getElementById('btn-compare');
        const btnReaction = document.getElementById('btn-reaction');

        btnCompare.addEventListener('click', () => {
            if (this.mode === 'compare') {
                this.setMode('info');
                btnCompare.classList.remove('active');
                btnCompare.textContent = "Enable Compare Mode";
            } else {
                this.setMode('compare');
                btnCompare.classList.add('active');
                btnCompare.textContent = "Exit Compare Mode";
                btnReaction.classList.remove('active');
                btnReaction.textContent = "Reaction Simulator";
            }
        });

        btnReaction.addEventListener('click', () => {
            if (this.mode === 'reaction') {
                this.setMode('info');
                btnReaction.classList.remove('active');
                btnReaction.textContent = "Reaction Simulator";
            } else {
                this.setMode('reaction');
                btnReaction.classList.add('active');
                btnReaction.textContent = "Exit Reaction Mode";
                btnCompare.classList.remove('active');
                btnCompare.textContent = "Enable Compare Mode";
            }
        });
    }

    setupSearch() {
        const searchBtn = document.getElementById('btn-search');
        const searchInput = document.getElementById('search-input');
        
        const executeSearch = () => {
            const query = searchInput.value.toLowerCase().trim();
            if (!query) return;

            const found = this.elements.find(el => el.name.toLowerCase() === query || el.sym.toLowerCase() === query || el.num.toString() === query);
            if (found) {
                const div = document.getElementById(`el-${found.num}`);
                if (div) {
                    this.handleClick(found, div);
                    div.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                alert('Element not found.');
            }
        };

        searchBtn.addEventListener('click', executeSearch);
        searchInput.addEventListener('keydown', e => { if (e.key === 'Enter') executeSearch(); });
    }

    setMode(mode) {
        this.mode = mode;
        this.ui.clearSelections();
        this.lockedElement = null;
        this.compareSelection = [];
        this.reactionSelection = [];
        this.dashboardUI.setMode(mode);
        if (mode === 'info') this.dashboardUI.resetInfo();
        if (mode === 'compare') this.dashboardUI.renderCompare([]);
        if (mode === 'reaction') this.dashboardUI.renderReactionSetup([], this.reactionType, this);
    }

    setReactionType(type) {
        this.reactionType = type;
        this.reactionSelection = [];
        this.ui.clearSelections();
        this.dashboardUI.renderReactionSetup(this.reactionSelection, this.reactionType, this);
        if (type === 'decomposition') this.runReaction();
    }

    setReactionCompound(compound) {
        this.reactionCompound = compound;
        if (this.reactionType === 'decomposition' || (this.reactionType === 'displacement' && this.reactionSelection.length === 1)) {
            this.runReaction();
        }
    }

    handleHover(el) {
        if (this.mode === 'info' && !this.lockedElement) {
            this.dashboardUI.renderInfo(el, false);
        }
    }

    handleHoverOut(el) {
        if (this.mode === 'info' && !this.lockedElement) {
            this.dashboardUI.resetInfo();
        } else if (this.mode === 'info' && this.lockedElement) {
            this.dashboardUI.renderInfo(this.lockedElement, true);
        }
    }

    handleClick(el, div) {
        if (this.mode === 'info') {
            if (this.lockedElement === el) {
                this.lockedElement = null;
                div.classList.remove('locked');
            } else {
                if (this.lockedElement) {
                    document.getElementById(`el-${this.lockedElement.num}`).classList.remove('locked');
                }
                this.lockedElement = el;
                div.classList.add('locked');
                this.dashboardUI.renderInfo(el, true);
            }
        } else if (this.mode === 'compare') {
            const index = this.compareSelection.findIndex(e => e.num === el.num);
            if (index > -1) {
                this.compareSelection.splice(index, 1); div.classList.remove('selected');
            } else {
                if (this.compareSelection.length >= 2) {
                    const removed = this.compareSelection.shift();
                    document.getElementById(`el-${removed.num}`).classList.remove('selected');
                }
                this.compareSelection.push(el); div.classList.add('selected');
            }
            this.dashboardUI.renderCompare(this.compareSelection);
        } else if (this.mode === 'reaction') {
            if (this.reactionType === 'decomposition') return; // no element selection needed

            const index = this.reactionSelection.findIndex(e => e.num === el.num);
            if (index > -1) {
                this.reactionSelection.splice(index, 1); div.classList.remove('reacting');
            } else {
                if (this.reactionType === 'combination' && this.reactionSelection.length >= 2) {
                    const removed = this.reactionSelection.shift();
                    document.getElementById(`el-${removed.num}`).classList.remove('reacting');
                } else if (this.reactionType !== 'combination' && this.reactionSelection.length >= 1) {
                    const removed = this.reactionSelection.shift();
                    document.getElementById(`el-${removed.num}`).classList.remove('reacting');
                }
                this.reactionSelection.push(el); div.classList.add('reacting');
            }
            this.dashboardUI.renderReactionSetup(this.reactionSelection, this.reactionType, this);
            
            if (this.reactionType === 'combination' && this.reactionSelection.length === 2) this.runReaction();
            if ((this.reactionType === 'displacement' || this.reactionType === 'acidbase') && this.reactionSelection.length === 1) this.runReaction();
        }
    }

    runReaction() {
        let result;
        if (this.reactionType === 'combination') {
            result = this.reactionEngine.predictCombination(this.reactionSelection[0], this.reactionSelection[1]);
        } else if (this.reactionType === 'displacement') {
            result = this.reactionEngine.checkDisplacement(this.reactionSelection[0], this.reactionCompound);
        } else if (this.reactionType === 'decomposition') {
            result = this.reactionEngine.getDecomposition(this.reactionCompound);
        } else if (this.reactionType === 'acidbase') {
            result = this.reactionEngine.getAcidBase(this.reactionSelection[0]);
        }

        let html = '';
        if (result.error) {
            html = `<div class="reaction-formula" style="color: #ef4444; border-color: #ef4444;">❌ ${result.error}</div>`;
        } else {
            html = `
                <div class="reaction-formula">${result.equation}</div>
                <p style="text-align: center; color: #d1d5db;">${result.desc}</p>
            `;
        }
        this.dashboardUI.renderReactionResult(html);
    }
}

// Initialize application on DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    new AppController();
});
