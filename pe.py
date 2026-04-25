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
        # ==========================================
        # 1. Basic / Electro-positive Radicals
        # ==========================================
        self.metals = {
            'H (Hydrogen)': 1, 'Li (Lithium)': 1, 'Na (Sodium)': 1, 'K (Potassium)': 1, 'Rb (Rubidium)': 1, 'Cs (Cesium)': 1, 
            'Ag (Silver)': 1, 'Cu_I (Cuprous)': 1, 'Au_I (Aurous)': 1, 'NH4 (Ammonium)': 1, 'Hg_I (Mercurous)': 1,
            'Be (Beryllium)': 2, 'Mg (Magnesium)': 2, 'Ca (Calcium)': 2, 'Sr (Strontium)': 2, 'Ba (Barium)': 2, 
            'Zn (Zinc)': 2, 'Cd (Cadmium)': 2, 'Ni (Nickel)': 2, 'Cu_II (Cupric)': 2, 'Fe_II (Ferrous)': 2, 
            'Co_II (Cobaltous)': 2, 'Hg_II (Mercuric)': 2, 'Sn_II (Stannous)': 2, 'Pb_II (Plumbous)': 2, 'Mn_II (Manganese)': 2,
            'Al (Aluminum)': 3, 'Fe_III (Ferric)': 3, 'Cr_III (Chromium)': 3, 'Ga (Gallium)': 3, 'In (Indium)': 3, 
            'Bi (Bismuth)': 3, 'Au_III (Auric)': 3, 'Co_III (Cobaltic)': 3, 'Sb_III (Antimony)': 3, 'As_III (Arsenic)': 3,
            'Ti_IV (Titanium)': 4, 'Sn_IV (Stannic)': 4, 'Pb_IV (Plumbic)': 4, 'Zr (Zirconium)': 4, 'Pt (Platinum)': 4, 
            'U_IV (Uranium)': 4, 'Th (Thorium)': 4,
            'W_VI (Tungsten)': 6
        }
        
        # ==========================================
        # 2. Acidic / Electro-negative Radicals
        # ==========================================
        self.nonmetals = {
            # Monovalent (1)
            'F (Fluoride)': 1, 'Cl (Chloride)': 1, 'Br (Bromide)': 1, 'I (Iodide)': 1, 
            'OH (Hydroxide)': 1, 'NO3 (Nitrate)': 1, 'NO2 (Nitrite)': 1, 'HCO3 (Bicarbonate)': 1, 
            'ClO3 (Chlorate)': 1, 'ClO (Hypochlorite)': 1, 'BrO (Hypobromite)': 1, 'IO (Hypoiodite)': 1, 
            'IO3 (Iodate)': 1, 'HSO3 (Bisulphite)': 1, 'HSO4 (Bisulphate)': 1, 'H (Hydride)': 1, 
            'CH3COO (Acetate)': 1, 'CN (Cyanide)': 1, 'MnO4 (Permanganate)': 1, 'AlO2 (Meta-aluminate)': 1,
            # Divalent (2)
            'O (Oxide)': 2, 'S (Sulphide)': 2, 'Se (Selenide)': 2, 'SO4 (Sulphate)': 2, 'SO3 (Sulphite)': 2, 
            'CO3 (Carbonate)': 2, 'CrO4 (Chromate)': 2, 'Cr2O7 (Dichromate)': 2, 'O2 (Peroxide)': 2, 
            'S2O3 (Thiosulphate)': 2, 'MnO4_2 (Manganate)': 2, 'ZnO2 (Zincate)': 2, 'SnO3 (Stannate)': 2, 
            'SiO3 (Silicate)': 2,
            # Trivalent (3)
            'N (Nitride)': 3, 'P (Phosphide)': 3, 'PO4 (Phosphate)': 3, 'PO3 (Phosphite)': 3, 
            'As (Arsenide)': 3, 'BO3 (Borate)': 3, 'Fe(CN)6_3 (Ferricyanide)': 3, 'AsO3 (Arsenite)': 3, 
            'AsO4 (Arsenate)': 3, 'AlO3 (Aluminate)': 3,
            # Tetravalent (4)
            'C (Carbide)': 4, 'Si (Silicide)': 4, 'Fe(CN)6_4 (Ferrocyanide)': 4
        }
        
        # Expanded Compounds (Added Water)
        self.compounds = {
            'H2O (Water)': ('H (Hydrogen)', 'O (Oxide)'),
            'NaCl (Sodium Chloride)': ('Na (Sodium)', 'Cl (Chloride)'), 'KCl (Potassium Chloride)': ('K (Potassium)', 'Cl (Chloride)'), 'AgCl (Silver Chloride)': ('Ag (Silver)', 'Cl (Chloride)'),
            'MgCl2 (Magnesium Chloride)': ('Mg (Magnesium)', 'Cl (Chloride)'), 'CaCl2 (Calcium Chloride)': ('Ca (Calcium)', 'Cl (Chloride)'), 'BaCl2 (Barium Chloride)': ('Ba (Barium)', 'Cl (Chloride)'),
            'CuCl2 (Copper II Chloride)': ('Cu_II (Cupric)', 'Cl (Chloride)'), 'FeCl3 (Iron III Chloride)': ('Fe_III (Ferric)', 'Cl (Chloride)'), 'AlCl3 (Aluminum Chloride)': ('Al (Aluminum)', 'Cl (Chloride)'),
            'Na2SO4 (Sodium Sulfate)': ('Na (Sodium)', 'SO4 (Sulphate)'), 'K2SO4 (Potassium Sulfate)': ('K (Potassium)', 'SO4 (Sulphate)'),
            'CaSO4 (Calcium Sulfate)': ('Ca (Calcium)', 'SO4 (Sulphate)'), 'BaSO4 (Barium Sulfate)': ('Ba (Barium)', 'SO4 (Sulphate)'),
            'CuSO4 (Copper Sulfate)': ('Cu_II (Cupric)', 'SO4 (Sulphate)'), 'ZnSO4 (Zinc Sulfate)': ('Zn (Zinc)', 'SO4 (Sulphate)'), 'FeSO4 (Iron II Sulfate)': ('Fe_II (Ferrous)', 'SO4 (Sulphate)'),
            'NaNO3 (Sodium Nitrate)': ('Na (Sodium)', 'NO3 (Nitrate)'), 'KNO3 (Potassium Nitrate)': ('K (Potassium)', 'NO3 (Nitrate)'), 'AgNO3 (Silver Nitrate)': ('Ag (Silver)', 'NO3 (Nitrate)'),
            'Pb(NO3)2 (Lead Nitrate)': ('Pb_II (Plumbous)', 'NO3 (Nitrate)'), 'Ca(NO3)2 (Calcium Nitrate)': ('Ca (Calcium)', 'NO3 (Nitrate)'),
            'Na2CO3 (Sodium Carbonate)': ('Na (Sodium)', 'CO3 (Carbonate)'), 'K2CO3 (Potassium Carbonate)': ('K (Potassium)', 'CO3 (Carbonate)'),
            'CaCO3 (Calcium Carbonate)': ('Ca (Calcium)', 'CO3 (Carbonate)'), 'MgCO3 (Magnesium Carbonate)': ('Mg (Magnesium)', 'CO3 (Carbonate)'),
            'NaHCO3 (Sodium Bicarbonate)': ('Na (Sodium)', 'HCO3 (Bicarbonate)'),
            'Na3PO4 (Sodium Phosphate)': ('Na (Sodium)', 'PO4 (Phosphate)'), 'Ca3(PO4)2 (Calcium Phosphate)': ('Ca (Calcium)', 'PO4 (Phosphate)'),
            'CuO (Copper II Oxide)': ('Cu_II (Cupric)', 'O (Oxide)'), 'ZnO (Zinc Oxide)': ('Zn (Zinc)', 'O (Oxide)'), 'MgO (Magnesium Oxide)': ('Mg (Magnesium)', 'O (Oxide)')
        }

        # Hybridization Mapping for Molecular Geometry
        self.hybridization_map = {
            'H2O': 'sp3', 'SO4': 'sp3', 'PO4': 'sp3', 'OH': 'sp3', 'ClO3': 'sp3', 
            'NH4': 'sp3', 'CH3COO': 'sp3', 'ClO': 'sp3', 'BrO': 'sp3', 'IO': 'sp3',
            'IO3': 'sp3', 'HSO3': 'sp3', 'HSO4': 'sp3', 'MnO4': 'sp3', 'CrO4': 'sp3',
            'Cr2O7': 'sp3', 'S2O3': 'sp3', 'AsO3': 'sp3', 'AsO4': 'sp3', 'PO3': 'sp3',
            'NO3': 'sp2', 'CO3': 'sp2', 'SO3': 'sp2', 'NO2': 'sp2', 'HCO3': 'sp2', 'BO3': 'sp2',
            'CN': 'sp', 'CO2': 'sp'
        }

        self.acids = {
            'HCl (Hydrochloric Acid)': 'Cl (Chloride)', 'HNO3 (Nitric Acid)': 'NO3 (Nitrate)', 'HBr (Hydrobromic Acid)': 'Br (Bromide)',
            'HI (Hydroiodic Acid)': 'I (Iodide)', 'HF (Hydrofluoric Acid)': 'F (Fluoride)',
            'H2SO4 (Sulfuric Acid)': 'SO4 (Sulphate)', 'H2CO3 (Carbonic Acid)': 'CO3 (Carbonate)',
            'H3PO4 (Phosphoric Acid)': 'PO4 (Phosphate)'
        }
        
        self.bases = {
            'NaOH (Sodium Hydroxide)': 'Na (Sodium)', 'KOH (Potassium Hydroxide)': 'K (Potassium)', 'LiOH (Lithium Hydroxide)': 'Li (Lithium)',
            'Ca(OH)2 (Calcium Hydroxide)': 'Ca (Calcium)', 'Mg(OH)2 (Magnesium Hydroxide)': 'Mg (Magnesium)', 'Ba(OH)2 (Barium Hydroxide)': 'Ba (Barium)',
            'Al(OH)3 (Aluminum Hydroxide)': 'Al (Aluminum)', 'Fe(OH)3 (Iron III Hydroxide)': 'Fe_III (Ferric)', 'Cu(OH)2 (Copper II Hydroxide)': 'Cu_II (Cupric)'
        }

        self.decomposition_targets = {
            'CaCO3 (Calcium Carbonate)': 'CaO + CO2',
            'H2O2 (Hydrogen Peroxide)': 'H2O + O2',
            'KClO3 (Potassium Chlorate)': 'KCl + O2',
            'H2O (Water via Electrolysis)': 'H2 + O2',
            'MgCO3 (Magnesium Carbonate)': 'MgO + CO2',
            'CuCO3 (Copper Carbonate)': 'CuO + CO2',
            'Ag2O (Silver Oxide)': 'Ag + O2'
        }

        self.reactivity_series = {
            'Li': 1, 'K': 2, 'Ba': 3, 'Sr': 4, 'Ca': 5, 'Na': 6, 'Mg': 7, 
            'Al': 8, 'Mn': 9, 'Zn': 10, 'Cr': 11, 'Fe': 12, 'Cd': 13, 
            'Co': 14, 'Ni': 15, 'Sn': 16, 'Pb': 17, 'H': 18, 
            'Cu': 19, 'Ag': 20, 'Hg': 21, 'Pt': 22, 'Au': 23
        }

    def check_solubility(self, cation, anion):
        """Returns True if the compound is soluble (aq), False if insoluble precipitate (s)."""
        c_base = cation.split('_')[0].split(' ')[0]
        a_base = anion.split('_')[0].split(' ')[0]
        
        if c_base in ['Li', 'Na', 'K', 'Rb', 'Cs', 'NH4', 'H']: return True
        if a_base in ['NO3', 'ClO3', 'CH3COO', 'HCO3', 'MnO4', 'ClO', 'BrO', 'IO', 'IO3', 'HSO3', 'HSO4']: return True
        if a_base in ['Cl', 'Br', 'I', 'CN']:
            if c_base in ['Ag', 'Pb', 'Hg']: return False
            return True
        if a_base == 'SO4':
            if c_base in ['Ba', 'Pb', 'Ca', 'Sr']: return False
            return True
        if a_base in ['CO3', 'PO4', 'OH', 'PO3', 'O', 'S', 'CrO4', 'Cr2O7', 'SO3', 'S2O3', 'SiO3', 'BO3', 'AsO3', 'AsO4', 'AlO3', 'Fe(CN)6', 'ZnO2', 'SnO3', 'AlO2']:
            return False
            
        return True

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
        polyatomics = ['OH', 'NO3', 'NO2', 'HCO3', 'ClO3', 'MnO4', 'SO4', 'SO3', 'CO3', 'CrO4', 'Cr2O7', 'PO4', 'PO3', 'NH4', 'CH3COO', 'CN', 'SiO3', 'S2O3', 'ClO', 'BrO', 'IO', 'IO3', 'HSO3', 'HSO4', 'AlO2', 'O2', 'MnO4', 'ZnO2', 'SnO3', 'BO3', 'AsO3', 'AsO4', 'AlO3', 'Fe(CN)6']
        
        c_clean = cation_key.split(' ')[0].split('_')[0]
        a_clean = anion_key.split(' ')[0].split('_')[0]
        
        v1 = self.metals[cation_key]
        v2 = self.nonmetals[anion_key]
        
        common_divisor = math.gcd(v1, v2)
        v1_simp = v1 // common_divisor
        v2_simp = v2 // common_divisor
        
        if v2_simp > 1:
            part1 = f"({c_clean}){v2_simp}" if c_clean in polyatomics else f"{c_clean}{v2_simp}"
        else:
            part1 = c_clean
            
        if v1_simp > 1:
            part2 = f"({a_clean}){v1_simp}" if a_clean in polyatomics else f"{a_clean}{v1_simp}"
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
        self.render_orbital_viewer()

    def get_orbital_svg(self, block, size=150):
        if block == 's':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-pulse 4s infinite ease-in-out;">
                <circle cx="50" cy="50" r="35" fill="url(#s-grad)" opacity="0.9" />
                <defs>
                    <radialGradient id="s-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="#fbbf24" stop-opacity="0" />
                    </radialGradient>
                </defs>
            </svg>'''
        elif block == 'p':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-spin 10s infinite linear; transform-origin: center;">
                <path d="M 50 50 C 20 0, 80 0, 50 50 C 20 100, 80 100, 50 50" fill="url(#p-grad)" opacity="0.9" />
                <defs>
                    <radialGradient id="p-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
                    </radialGradient>
                </defs>
            </svg>'''
        elif block == 'd':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-spin 14s infinite linear; transform-origin: center;">
                <path d="M 50 50 C 20 0, 80 0, 50 50 C 20 100, 80 100, 50 50 M 50 50 C 0 20, 0 80, 50 50 C 100 20, 100 80, 50 50" fill="url(#d-grad)" opacity="0.9" />
                <defs>
                    <radialGradient id="d-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#10b981" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
                    </radialGradient>
                </defs>
            </svg>'''
        elif block == 'f':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-spin 18s infinite linear reverse; transform-origin: center;">
                <path d="M 50 50 C 30 0, 70 0, 50 50 C 80 0, 100 40, 50 50 C 100 60, 80 100, 50 50 C 70 100, 30 100, 50 50 C 20 100, 0 60, 50 50 C 0 40, 20 0, 50 50" fill="url(#f-grad)" opacity="0.9" />
                <defs>
                    <radialGradient id="f-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0" />
                    </radialGradient>
                </defs>
            </svg>'''
        return ''

    def get_hybridization_svg(self, hybrid_type, size=150):
        color = "#ec4899"
        if hybrid_type == 'sp':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-pulse 4s infinite ease-in-out;">
                <path d="M 50 50 C 30 30, 10 30, 10 50 C 10 70, 30 70, 50 50" fill="url(#hyb-grad)" opacity="0.9" />
                <path d="M 50 50 C 70 30, 90 30, 90 50 C 90 70, 70 70, 50 50" fill="url(#hyb-grad)" opacity="0.9" />
                <circle cx="50" cy="50" r="5" fill="#fff" opacity="0.8" />
                <defs>
                    <radialGradient id="hyb-grad" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="{color}" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="{color}" stop-opacity="0" />
                    </radialGradient>
                </defs>
            </svg>'''
        elif hybrid_type == 'sp2':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-spin 10s infinite linear; transform-origin: center;">
                <defs>
                    <radialGradient id="hyb-grad-sp2" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="{color}" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="{color}" stop-opacity="0" />
                    </radialGradient>
                    <path id="sp2-lobe" d="M 50 50 C 30 30, 30 5, 50 5 C 70 5, 70 30, 50 50" fill="url(#hyb-grad-sp2)" opacity="0.9" />
                </defs>
                <use href="#sp2-lobe" />
                <use href="#sp2-lobe" transform="rotate(120 50 50)" />
                <use href="#sp2-lobe" transform="rotate(240 50 50)" />
                <circle cx="50" cy="50" r="5" fill="#fff" opacity="0.8" />
            </svg>'''
        elif hybrid_type == 'sp3':
            return f'''<svg viewBox="0 0 100 100" width="{size}" height="{size}" style="animation: hybrid-spin 14s infinite linear reverse; transform-origin: center;">
                <defs>
                    <radialGradient id="hyb-grad-sp3" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="{color}" stop-opacity="0.9" />
                        <stop offset="100%" stop-color="{color}" stop-opacity="0" />
                    </radialGradient>
                    <path id="sp3-lobe" d="M 50 50 C 35 30, 35 5, 50 5 C 65 5, 65 30, 50 50" fill="url(#hyb-grad-sp3)" opacity="0.9" />
                </defs>
                <use href="#sp3-lobe" transform="rotate(140 50 50)" />
                <use href="#sp3-lobe" transform="rotate(220 50 50)" />
                <use href="#sp3-lobe" transform="rotate(180 50 50)" opacity="0.4" />
                <use href="#sp3-lobe" />
                <circle cx="50" cy="50" r="5" fill="#fff" opacity="0.8" />
            </svg>'''
        return ''

    def render_orbital_viewer(self):
        st.sidebar.markdown("---")
        st.sidebar.header("⚛️ Orbital & Hybridization Viewer")
        
        st.sidebar.markdown("""
        <style>
        @keyframes hybrid-spin {
            0% { transform: rotate(0deg) scale(0.95); }
            50% { transform: rotate(180deg) scale(1.05); }
            100% { transform: rotate(360deg) scale(0.95); }
        }
        @keyframes hybrid-pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        </style>
        """, unsafe_allow_html=True)

        view_type = st.sidebar.radio("View Mode", ["Metals (Orbitals)", "Nonmetals (Orbitals)", "Compounds (Hybridization)"])
        
        if view_type == "Metals (Orbitals)":
            choice = st.sidebar.selectbox("Select Metal", list(self.metals.keys()))
            c_base = choice.split('_')[0].split(' ')[0]
            
            if c_base in self.hybridization_map:
                hyb = self.hybridization_map[c_base]
                st.sidebar.markdown(f"<div style='text-align: center; color: #ec4899; margin-bottom: 20px;'><h3>{c_base} ({hyb} Hybridization)</h3></div>", unsafe_allow_html=True)
                st.sidebar.markdown(f"<div style='display: flex; justify-content: center;'>{self.get_hybridization_svg(hyb)}</div>", unsafe_allow_html=True)
            else:
                s_block = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Be', 'Mg', 'Ca', 'Sr', 'Ba', 'H']
                p_block = ['Al', 'Ga', 'In', 'Sn', 'Tl', 'Pb', 'Bi']
                f_block = ['U', 'Th']
                
                block = 's' if c_base in s_block else 'p' if c_base in p_block else 'f' if c_base in f_block else 'd'
                
                st.sidebar.markdown(f"<div style='text-align: center; color: var(--text-main); margin-bottom: 20px;'><h3>{c_base} ({block}-orbital)</h3></div>", unsafe_allow_html=True)
                st.sidebar.markdown(f"<div style='display: flex; justify-content: center;'>{self.get_orbital_svg(block)}</div>", unsafe_allow_html=True)
            
        elif view_type == "Nonmetals (Orbitals)":
            choice = st.sidebar.selectbox("Select Nonmetal", list(self.nonmetals.keys()))
            c_base = choice.split('_')[0].split(' ')[0]
            
            if c_base in self.hybridization_map:
                hyb = self.hybridization_map[c_base]
                st.sidebar.markdown(f"<div style='text-align: center; color: #ec4899; margin-bottom: 20px;'><h3>{c_base} ({hyb} Hybridization)</h3></div>", unsafe_allow_html=True)
                st.sidebar.markdown(f"<div style='display: flex; justify-content: center;'>{self.get_hybridization_svg(hyb)}</div>", unsafe_allow_html=True)
            else:
                block = 's' if c_base == 'H' else 'p'
                
                st.sidebar.markdown(f"<div style='text-align: center; color: var(--text-main); margin-bottom: 20px;'><h3>{c_base} ({block}-orbital)</h3></div>", unsafe_allow_html=True)
                st.sidebar.markdown(f"<div style='display: flex; justify-content: center;'>{self.get_orbital_svg(block)}</div>", unsafe_allow_html=True)
            
        else:
            choice = st.sidebar.selectbox("Select Compound", list(self.compounds.keys()))
            
            hyb = 'Ionic'
            comp_name = choice.split(' ')[0]
            
            if comp_name in self.hybridization_map:
                hyb = self.hybridization_map[comp_name]
            else:
                cation_base = self.compounds[choice][0].split(' ')[0]
                anion_base = self.compounds[choice][1].split(' ')[0]
                
                if cation_base in self.hybridization_map:
                    hyb = self.hybridization_map[cation_base]
                elif anion_base in self.hybridization_map:
                    hyb = self.hybridization_map[anion_base]
            
            if hyb == 'Ionic':
                st.sidebar.info(f"{comp_name} is primarily an ionic network or lacks a distinct covalent central atom for hybridization display.")
            else:
                st.sidebar.markdown(f"<div style='text-align: center; color: #ec4899; margin-bottom: 20px;'><h3>{comp_name} ({hyb})</h3></div>", unsafe_allow_html=True)
                st.sidebar.markdown(f"<div style='display: flex; justify-content: center;'>{self.get_hybridization_svg(hyb)}</div>", unsafe_allow_html=True)

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
                    a_base = nonmetal.split('_')[0].split(' ')[0]
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
