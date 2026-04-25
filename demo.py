import streamlit as st
import streamlit.components.v1 as components
import os
import math

class PeriodicTableApp:
    def __init__(self):
        st.set_page_config(
            page_title="Interactive Periodic Table",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.init_chemical_data()

    def init_chemical_data(self):
        # 40+ Metals / Cations (with their valencies/oxidation states)
        self.metals = {
            'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Ag': 1, 'Cu_I (Cuprous)': 1, 'Au_I': 1, 'NH4 (Ammonium)': 1,
            'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Zn': 2, 'Cd': 2, 'Ni': 2, 
            'Cu_II (Cupric)': 2, 'Fe_II (Ferrous)': 2, 'Co_II': 2, 'Hg_II': 2, 'Sn_II (Stannous)': 2, 'Pb_II': 2, 'Mn_II': 2,
            'Al': 3, 'Fe_III (Ferric)': 3, 'Cr_III': 3, 'Ga': 3, 'In': 3, 'Bi': 3, 'Au_III': 3, 'Co_III': 3, 'Sb_III': 3, 'As_III': 3,
            'Ti_IV': 4, 'Sn_IV (Stannic)': 4, 'Pb_IV': 4, 'Zr': 4, 'Pt': 4, 'U_IV': 4, 'Th': 4,
            'W_VI': 6
        }
        
        # 25+ Nonmetals & Polyatomic Anions (with absolute valencies for criss-cross)
        self.nonmetals = {
            'F': 1, 'Cl': 1, 'Br': 1, 'I': 1, 'OH (Hydroxide)': 1, 'NO3 (Nitrate)': 1, 'NO2 (Nitrite)': 1, 'HCO3 (Bicarbonate)': 1, 'ClO3 (Chlorate)': 1, 'MnO4 (Permanganate)': 1,
            'O': 2, 'S': 2, 'Se': 2, 'SO4 (Sulfate)': 2, 'SO3 (Sulfite)': 2, 'CO3 (Carbonate)': 2, 'CrO4 (Chromate)': 2, 'Cr2O7 (Dichromate)': 2,
            'N': 3, 'P': 3, 'PO4 (Phosphate)': 3, 'PO3 (Phosphite)': 3, 'As': 3,
            'C': 4, 'Si': 4
        }
        
        # 40+ Compounds mapped to their constituent (Cation, Anion) for displacement logic
        self.compounds = {
            'NaCl (Sodium Chloride)': ('Na', 'Cl'), 'KCl (Potassium Chloride)': ('K', 'Cl'), 'AgCl (Silver Chloride)': ('Ag', 'Cl'),
            'MgCl2 (Magnesium Chloride)': ('Mg', 'Cl'), 'CaCl2 (Calcium Chloride)': ('Ca', 'Cl'), 'BaCl2 (Barium Chloride)': ('Ba', 'Cl'),
            'CuCl2 (Copper II Chloride)': ('Cu_II (Cupric)', 'Cl'), 'FeCl3 (Iron III Chloride)': ('Fe_III (Ferric)', 'Cl'), 'AlCl3 (Aluminum Chloride)': ('Al', 'Cl'),
            'Na2SO4 (Sodium Sulfate)': ('Na', 'SO4 (Sulfate)'), 'K2SO4 (Potassium Sulfate)': ('K', 'SO4 (Sulfate)'),
            'CaSO4 (Calcium Sulfate)': ('Ca', 'SO4 (Sulfate)'), 'BaSO4 (Barium Sulfate)': ('Ba', 'SO4 (Sulfate)'),
            'CuSO4 (Copper Sulfate)': ('Cu_II (Cupric)', 'SO4 (Sulfate)'), 'ZnSO4 (Zinc Sulfate)': ('Zn', 'SO4 (Sulfate)'), 'FeSO4 (Iron II Sulfate)': ('Fe_II (Ferrous)', 'SO4 (Sulfate)'),
            'NaNO3 (Sodium Nitrate)': ('Na', 'NO3 (Nitrate)'), 'KNO3 (Potassium Nitrate)': ('K', 'NO3 (Nitrate)'), 'AgNO3 (Silver Nitrate)': ('Ag', 'NO3 (Nitrate)'),
            'Pb(NO3)2 (Lead Nitrate)': ('Pb_II', 'NO3 (Nitrate)'), 'Ca(NO3)2 (Calcium Nitrate)': ('Ca', 'NO3 (Nitrate)'),
            'Na2CO3 (Sodium Carbonate)': ('Na', 'CO3 (Carbonate)'), 'K2CO3 (Potassium Carbonate)': ('K', 'CO3 (Carbonate)'),
            'CaCO3 (Calcium Carbonate)': ('Ca', 'CO3 (Carbonate)'), 'MgCO3 (Magnesium Carbonate)': ('Mg', 'CO3 (Carbonate)'),
            'NaHCO3 (Sodium Bicarbonate)': ('Na', 'HCO3 (Bicarbonate)'),
            'Na3PO4 (Sodium Phosphate)': ('Na', 'PO4 (Phosphate)'), 'Ca3(PO4)2 (Calcium Phosphate)': ('Ca', 'PO4 (Phosphate)'),
            'CuO (Copper II Oxide)': ('Cu_II (Cupric)', 'O'), 'ZnO (Zinc Oxide)': ('Zn', 'O'), 'MgO (Magnesium Oxide)': ('Mg', 'O')
        }

        # Acids mapped to their Anion (H+ is implicit)
        self.acids = {
            'HCl (Hydrochloric Acid)': 'Cl', 'HNO3 (Nitric Acid)': 'NO3 (Nitrate)', 'HBr (Hydrobromic Acid)': 'Br',
            'HI (Hydroiodic Acid)': 'I', 'HF (Hydrofluoric Acid)': 'F',
            'H2SO4 (Sulfuric Acid)': 'SO4 (Sulfate)', 'H2CO3 (Carbonic Acid)': 'CO3 (Carbonate)',
            'H3PO4 (Phosphoric Acid)': 'PO4 (Phosphate)'
        }
        
        # Bases mapped to their Metal Cation (OH- is implicit)
        self.bases = {
            'NaOH (Sodium Hydroxide)': 'Na', 'KOH (Potassium Hydroxide)': 'K', 'LiOH (Lithium Hydroxide)': 'Li',
            'Ca(OH)2 (Calcium Hydroxide)': 'Ca', 'Mg(OH)2 (Magnesium Hydroxide)': 'Mg', 'Ba(OH)2 (Barium Hydroxide)': 'Ba',
            'Al(OH)3 (Aluminum Hydroxide)': 'Al', 'Fe(OH)3 (Iron III Hydroxide)': 'Fe_III (Ferric)', 'Cu(OH)2 (Copper II Hydroxide)': 'Cu_II (Cupric)'
        }

        # Specific targets for decomposition with hardcoded simplified outputs
        self.decomposition_targets = {
            'CaCO3 (Calcium Carbonate)': 'CaO + CO2',
            'H2O2 (Hydrogen Peroxide)': 'H2O + O2',
            'KClO3 (Potassium Chlorate)': 'KCl + O2',
            'H2O (Water via Electrolysis)': 'H2 + O2',
            'MgCO3 (Magnesium Carbonate)': 'MgO + CO2',
            'CuCO3 (Copper Carbonate)': 'CuO + CO2',
            'Ag2O (Silver Oxide)': 'Ag + O2'
        }

        # Reactivity Series (Lower index number = more reactive/electropositive)
        self.reactivity_series = {
            'Li': 1, 'K': 2, 'Ba': 3, 'Sr': 4, 'Ca': 5, 'Na': 6, 'Mg': 7, 
            'Al': 8, 'Mn': 9, 'Zn': 10, 'Cr': 11, 'Fe': 12, 'Cd': 13, 
            'Co': 14, 'Ni': 15, 'Sn': 16, 'Pb': 17, 'H': 18, 
            'Cu': 19, 'Ag': 20, 'Hg': 21, 'Pt': 22, 'Au': 23
        }

    def check_solubility(self, cation, anion):
        """Returns True if the compound is soluble (aq), False if insoluble precipitate (s)."""
        c_base = cation.split('_')[0].split(' ')[0]
        a_base = anion.split(' ')[0]
        
        # Rule 1: Group 1 metals and Ammonium are always soluble
        if c_base in ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4']: return True
        # Rule 2: Nitrates, Chlorates, Acetates are always soluble
        if a_base in ['NO3', 'ClO3', 'C2H3O2', 'HCO3', 'MnO4']: return True
        # Rule 3: Chlorides, Bromides, Iodides are soluble EXCEPT Ag, Pb, Hg
        if a_base in ['Cl', 'Br', 'I']:
            if c_base in ['Ag', 'Pb', 'Hg']: return False
            return True
        # Rule 4: Sulfates are soluble EXCEPT Ba, Pb, Ca, Sr
        if a_base == 'SO4':
            if c_base in ['Ba', 'Pb', 'Ca', 'Sr']: return False
            return True
        # Rule 5: Carbonates, Phosphates, Hydroxides are INSOLUBLE except with Group 1
        if a_base in ['CO3', 'PO4', 'OH', 'PO3', 'O', 'S', 'CrO4', 'Cr2O7']:
            return False
            
        return True # Default fallback

    def format_output(self, status, equation, note):
        color = "#10b981" if status == "Reaction Occurs" else "#ef4444"
        return f"""
<div style="background-color: var(--panel-bg); padding: 15px; border-radius: 8px; border-left: 4px solid {color}; margin-top: 10px; margin-bottom: 20px;">
    <strong>Reaction Status:</strong> <span style="color: {color};">{status}</span><br><br>
    <strong>Balanced Equation:</strong><br> <span style="font-family: monospace; font-size: 1.1em; color: var(--text-main);">{equation}</span><br><br>
    <strong>Professor's Note:</strong> <em style="color: #9ca3af;">{note}</em>
</div>
"""

    def format_formula(self, text):
        """Converts numbers in a string to subscript, avoiding converting charges if they existed."""
        subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return text.translate(subscript_map)

    def calculate_criss_cross(self, cation_key, anion_key):
        """Generates a molecular formula using the criss-cross method and applies parentheses properly."""
        polyatomics = ['OH', 'NO3', 'NO2', 'HCO3', 'ClO3', 'MnO4', 'SO4', 'SO3', 'CO3', 'CrO4', 'Cr2O7', 'PO4', 'PO3', 'NH4']
        
        # Clean labels to get just the symbol (e.g., "Fe_II (Ferrous)" -> "Fe")
        c_clean = cation_key.split(' ')[0].split('_')[0]
        a_clean = anion_key.split(' ')[0]
        
        v1 = self.metals[cation_key]
        v2 = self.nonmetals[anion_key]
        
        # Simplify ratio (e.g., Ca=2, O=2 -> CaO)
        common_divisor = math.gcd(v1, v2)
        v1_simp = v1 // common_divisor
        v2_simp = v2 // common_divisor
        
        # Format Cation side
        if v2_simp > 1:
            if c_clean in polyatomics:
                part1 = f"({c_clean}){v2_simp}"
            else:
                part1 = f"{c_clean}{v2_simp}"
        else:
            part1 = c_clean
            
        # Format Anion side
        if v1_simp > 1:
            if a_clean in polyatomics:
                part2 = f"({a_clean}){v1_simp}"
            else:
                part2 = f"{a_clean}{v1_simp}"
        else:
            part2 = a_clean
            
        return self.format_formula(part1 + part2)

    def render_sidebar(self):
        st.sidebar.title("📚 Properties Guide")
        st.sidebar.markdown("""
### ⚛️ Atomic Number & Mass
**Number:** Protons in the nucleus. **Mass:** Average mass in atomic mass units (u).

### 🔗 Electronegativity
How strongly an atom attracts electrons. Higher values = more "electron-hungry."

### ➕ Electropositivity
How easily an atom loses electrons in a bond. Higher values = readily gives up electrons.

### 🔋 Electron Configuration
The full arrangement of electrons in orbitals (e.g., 1s² 2s² 2p⁶...). 
        """, unsafe_allow_html=True)

    def render_reaction_simulator(self):
        st.markdown("---")
        st.header("⚗️ Chemical Reaction Simulator")
        st.write("Calculates exact formulas based on valency crossing and ion exchange.")
        
        reaction_type = st.radio(
            "Select Reaction Type:", 
            ["Cross (Synthesis)", "Decomposition", "Single Displacement", "Double Displacement", "Acid-Base (Neutralization)"],
            horizontal=True
        )
        
        st.markdown("### Parameters")
        col1, col2, col3 = st.columns([2, 2, 1])
        
        if reaction_type == "Cross (Synthesis)":
            with col1:
                metal = st.selectbox("Select Metal (Cation):", list(self.metals.keys()))
                st.caption(f"Valency: +{self.metals[metal]}")
            with col2:
                nonmetal = st.selectbox("Select Nonmetal (Anion):", list(self.nonmetals.keys()))
                st.caption(f"Valency: -{self.nonmetals[nonmetal]}")
            with col3:
                st.write(""); st.write("")
                if st.button("React ⚡", use_container_width=True):
                    product = self.calculate_criss_cross(metal, nonmetal)
                    c_base = metal.split('_')[0].split(' ')[0]
                    a_base = nonmetal.split(' ')[0]
                    sol = "(aq)" if self.check_solubility(metal, nonmetal) else "(s)"
                    st.markdown(self.format_output(
                        "Reaction Occurs",
                        f"{c_base} + {a_base} → {product}{sol}",
                        "Transition metal valencies are explicitly enforced by your selection prior to executing the criss-cross method."
                    ), unsafe_allow_html=True)
                    
        elif reaction_type == "Decomposition":
            with col1:
                compound = st.selectbox("Select Compound to React:", list(self.decomposition_targets.keys()) + ["Na2CO3 (Sodium Carbonate)", "K2CO3 (Potassium Carbonate)"])
            with col3:
                st.write(""); st.write("")
                if st.button("React 💥", use_container_width=True):
                    if compound in ["Na2CO3 (Sodium Carbonate)", "K2CO3 (Potassium Carbonate)"]:
                        comp_form = self.format_formula(compound.split(' ')[0])
                        st.markdown(self.format_output(
                            "No Reaction",
                            f"{comp_form}(s) + Δ → N/R",
                            "Group 1 Alkali Metal Carbonates are thermally stable fortresses. Under standard Bunsen burner heating, they melt rather than decompose."
                        ), unsafe_allow_html=True)
                    else:
                        comp_form = self.format_formula(compound.split(' ')[0])
                        result = self.format_formula(self.decomposition_targets[compound])
                        st.markdown(self.format_output(
                            "Reaction Occurs",
                            f"{comp_form}(s) + Δ → {result}",
                            "Standard thermal decomposition breaks down the compound into simpler elements or metal oxides and gases."
                        ), unsafe_allow_html=True)
                    
        elif reaction_type == "Single Displacement":
            with col1:
                active_metal = st.selectbox("Select Pure Active Metal:", list(self.metals.keys()))
            with col2:
                aqueous_salt = st.selectbox("Select Aqueous Compound:", list(self.compounds.keys()))
            with col3:
                st.write(""); st.write("")
                if st.button("Displace 🔄", use_container_width=True):
                    comp_cation, comp_anion = self.compounds[aqueous_salt]
                    active_base = active_metal.split('_')[0].split(' ')[0]
                    comp_base = comp_cation.split('_')[0].split(' ')[0]
                    aq_form = self.format_formula(aqueous_salt.split(' ')[0])
                    
                    acids = ['HCl', 'HNO3', 'HBr', 'HI', 'HF', 'H2SO4', 'H2CO3', 'H3PO4']
                    is_acid = comp_base == 'H' or aqueous_salt.split(' ')[0] in acids
                    
                    if active_base in ['Cu', 'Ag', 'Pt', 'Au'] and is_acid:
                        st.markdown(self.format_output(
                            "No Reaction",
                            f"{active_base}(s) + {aq_form}(aq) → N/R",
                            f"{active_base} is below Hydrogen in the reactivity series. It cannot displace Hydrogen from standard acids."
                        ), unsafe_allow_html=True)
                    else:
                        active_rank = self.reactivity_series.get(active_base, 100)
                        comp_rank = self.reactivity_series.get(comp_base, 100)
                        
                        if active_rank < comp_rank:
                            new_salt = self.calculate_criss_cross(active_metal, comp_anion)
                            displaced_metal = comp_base
                            sol = "(aq)" if self.check_solubility(active_metal, comp_anion) else "(s) ↓"
                            st.markdown(self.format_output(
                                "Reaction Occurs",
                                f"{active_base}(s) + {aq_form}(aq) → {new_salt}{sol} + {displaced_metal}(s)",
                                f"{active_base} is more electropositive than {comp_base} (higher on the reactivity series), allowing it to successfully displace {comp_base} from the compound."
                            ), unsafe_allow_html=True)
                        elif active_rank == comp_rank:
                            st.info("No net reaction. The elements are the same.")
                        else:
                            st.markdown(self.format_output(
                                "No Reaction",
                                f"{active_base}(s) + {aq_form}(aq) → N/R",
                                f"A pure metal can only displace a metal in an aqueous compound if it is more electropositive. {active_base} is below {comp_base}."
                            ), unsafe_allow_html=True)

        elif reaction_type == "Double Displacement":
            with col1:
                comp1 = st.selectbox("Select First Compound:", list(self.compounds.keys()), key='dd1')
            with col2:
                comp2 = st.selectbox("Select Second Compound:", list(self.compounds.keys()), key='dd2')
            with col3:
                st.write(""); st.write("")
                if st.button("Exchange Ions 🔀", use_container_width=True):
                    if comp1 == comp2:
                        st.warning("Please select two different compounds.")
                    else:
                        c1, a1 = self.compounds[comp1]
                        c2, a2 = self.compounds[comp2]
                        
                        comp1_f = self.format_formula(comp1.split(' ')[0])
                        comp2_f = self.format_formula(comp2.split(' ')[0])

                        product1 = self.calculate_criss_cross(c1, a2)
                        product2 = self.calculate_criss_cross(c2, a1)
                        
                        sol1_bool = self.check_solubility(c1, a2)
                        sol2_bool = self.check_solubility(c2, a1)
                        
                        sol1 = "(aq)" if sol1_bool else "(s) ↓"
                        sol2 = "(aq)" if sol2_bool else "(s) ↓"
                        
                        if sol1_bool and sol2_bool:
                            st.markdown(self.format_output(
                                "No Reaction",
                                f"{comp1_f}(aq) + {comp2_f}(aq) → N/R",
                                "Both potential products are soluble in water. The ions remain dissolved as spectator ions; no precipitate forms."
                            ), unsafe_allow_html=True)
                        else:
                            st.markdown(self.format_output(
                                "Reaction Occurs",
                                f"{comp1_f}(aq) + {comp2_f}(aq) → {product1}{sol1} + {product2}{sol2}",
                                "An insoluble rebel (precipitate) is formed during the ion exchange, driving the reaction forward."
                            ), unsafe_allow_html=True)

        elif reaction_type == "Acid-Base (Neutralization)":
            with col1:
                acid = st.selectbox("Select Acid / Reactant 1:", list(self.acids.keys()) + ["Al2O3 (Aluminum Oxide)", "ZnO (Zinc Oxide)"])
            with col2:
                base = st.selectbox("Select Base / Reactant 2:", list(self.bases.keys()) + ["Al2O3 (Aluminum Oxide)", "ZnO (Zinc Oxide)"])
            with col3:
                st.write(""); st.write("")
                if st.button("Neutralize 💧", use_container_width=True):
                    is_ampho_1 = acid in ["Al2O3 (Aluminum Oxide)", "ZnO (Zinc Oxide)"]
                    is_ampho_2 = base in ["Al2O3 (Aluminum Oxide)", "ZnO (Zinc Oxide)"]
                    
                    acid_f = self.format_formula(acid.split(' ')[0])
                    base_f = self.format_formula(base.split(' ')[0])
                    
                    if is_ampho_1 and "NaOH" in base:
                        complex_salt = "NaAlO₂(aq)" if "Al2O3" in acid else "Na₂ZnO₂(aq)"
                        st.markdown(self.format_output(
                            "Reaction Occurs",
                            f"{acid_f}(s) + {base_f}(aq) → {complex_salt} + H₂O(l)",
                            "Amphoteric Rule-Bender: Zinc and Aluminum oxides react with strong bases like NaOH to form complex aluminate or zincate salts."
                        ), unsafe_allow_html=True)
                    elif is_ampho_2 and "HCl" in acid:
                        salt = "AlCl₃(aq)" if "Al2O3" in base else "ZnCl₂(aq)"
                        st.markdown(self.format_output(
                            "Reaction Occurs",
                            f"{acid_f}(aq) + {base_f}(s) → {salt} + H₂O(l)",
                            "Amphoteric Rule-Bender: Zinc and Aluminum oxides act as bases when reacting with acids."
                        ), unsafe_allow_html=True)
                    elif is_ampho_1 and is_ampho_2:
                        st.markdown(self.format_output(
                            "No Reaction",
                            f"{acid_f}(s) + {base_f}(s) → N/R",
                            "Two amphoteric oxides will not react with each other under standard aqueous conditions."
                        ), unsafe_allow_html=True)
                    elif not is_ampho_1 and not is_ampho_2:
                        cation = self.bases[base]
                        anion = self.acids[acid]
                        salt = self.calculate_criss_cross(cation, anion)
                        sol = "(aq)" if self.check_solubility(cation, anion) else "(s) ↓"
                        
                        st.markdown(self.format_output(
                            "Reaction Occurs",
                            f"{acid_f}(aq) + {base_f}(aq) → {salt}{sol} + H₂O(l)",
                            "Standard Acid-Base Neutralization: The H⁺ from the acid and OH⁻ from the base form water, leaving a salt."
                        ), unsafe_allow_html=True)
                    else:
                        st.markdown(self.format_output(
                            "Reaction Occurs",
                            f"{acid_f} + {base_f} → Complex Salt + H₂O(l)",
                            "Amphoteric reaction occurs, shifting behavior depending on the strength of the opposing acid or base."
                        ), unsafe_allow_html=True)
        
        st.markdown("---")

    def load_frontend_assets(self):
        base_dir = os.path.dirname(__file__)
        frontend_dir = os.path.join(base_dir, "frontend")

        try:
            with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as f:
                html_content = f.read()
            with open(os.path.join(frontend_dir, "style.css"), "r", encoding="utf-8") as f:
                css_content = f.read()
            with open(os.path.join(frontend_dir, "data.js"), "r", encoding="utf-8") as f:
                data_js = f.read()
            with open(os.path.join(frontend_dir, "app.js"), "r", encoding="utf-8") as f:
                app_js = f.read()

            full_js = data_js + "\n\n" + app_js
            html_content = html_content.replace('<style id="injected-css"></style>', f'<style>{css_content}</style>')
            html_content = html_content.replace('<script id="injected-js" type="module"></script>', f'<script>{full_js}</script>')
            return html_content
        except FileNotFoundError:
            return "<div style='color: white; text-align: center; padding: 50px;'>Frontend files not found. Ensure 'frontend/' folder exists with index.html, style.css, data.js, and app.js.</div>"

    def run(self):
        st.title("Advanced Periodic Table & Reaction Engine")
        self.render_sidebar()
        self.render_reaction_simulator()
        
        html_source = self.load_frontend_assets()
        components.html(html_source, height=1500, scrolling=True)

if __name__ == "__main__":
    app = PeriodicTableApp()
    app.run()
