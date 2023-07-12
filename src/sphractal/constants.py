BULK_CN = 12  # Assuming FCC/HCP packing
defRad = 1.0  # Default radius value for missing data
# Atomic radii (computed from theoretical models) from E. Clementi; D.L. Raimondi; W.P. Reinhardt (1967) "Atomic
# Screening Constants from SCF Functions. II. Atoms with 37 to 86 Electrons." The Journal of Chemical Physics. 47 (4):
# 1300-1307; 
# Recommendations of values for multipliers: {radMult: 1.2, alphaMult: 2.0}
# If radii are 20% larger, recommendations: {radMult: 1.0, alphaMult: 5/3}
ATOMIC_RAD_DICT = {
    'H': 0.53, 'He': 0.31, 'Li': 1.67, 'Be': 1.12, 'B': 0.87, 'C': 0.67, 'N': 0.56, 'O': 0.48, 'F': 0.42, 'Ne': 0.38,
    'Na': 1.90, 'Mg': 1.45, 'Al': 1.18, 'Si': 1.11, 'P': 0.98, 'S': 0.88, 'Cl': 0.79, 'Ar': 0.71, 'K': 2.43, 'Ca': 1.94,
    'Sc': 1.84, 'Ti': 1.76, 'V': 1.71, 'Cr': 1.66, 'Mn': 1.61, 'Fe': 1.56, 'Co': 1.52, 'Ni': 1.49, 'Cu': 1.45,
    'Zn': 1.42, 'Ga': 1.36, 'Ge': 1.25, 'As': 1.14, 'Se': 1.03, 'Br': 0.94, 'Kr': 0.88, 'Rb': 2.65, 'Sr': 2.19,
    'Y': 2.12, 'Zr': 2.06, 'Nb': 1.98, 'Mo': 1.90, 'Tc': 1.83, 'Ru': 1.78, 'Rh': 1.73, 'Pd': 1.69, 'Ag': 1.65,
    'Cd': 1.61, 'In': 1.56, 'Sn': 1.45, 'Sb': 1.33, 'Te': 1.23, 'I': 1.15, 'Xe': 1.08, 'Cs': 2.98, 'Ba': 2.53,
    'La': 2.26, 'Ce': 2.10, 'Pr': 2.47, 'Nd': 2.06, 'Pm': 2.05, 'Sm': 2.38, 'Eu': 2.31, 'Gd': 2.33, 'Tb': 2.25,
    'Dy': 2.28, 'Ho': 2.26, 'Er': 2.26, 'Tm': 2.22, 'Yb': 2.22, 'Lu': 2.17, 'Hf': 2.08, 'Ta': 2.00, 'W': 1.93,
    'Re': 1.88, 'Os': 1.85, 'Ir': 1.80, 'Pt': 1.77, 'Au': 1.74, 'Hg': 1.71, 'Tl': 1.56, 'Pb': 1.54, 'Bi': 1.43,
    'Po': 1.35, 'At': 1.27, 'Rn': 1.20, 'Fr': defRad, 'Ra': defRad, 'Ac': defRad, 'Th': defRad, 'Pa': defRad,
    'U': defRad, 'Np': defRad, 'Pu': defRad, 'Am': defRad, 'Cm': defRad, 'Bk': defRad, 'Cf': defRad, 'Es': defRad,
    'Fm': defRad, 'Md': defRad, 'No': defRad, 'Lr': defRad, 'Rf': defRad, 'Db': defRad, 'Sg': defRad, 'Bh': defRad,
    'Hs': defRad, 'Mt': defRad, 'Ds': defRad, 'Rg': defRad, 'Cn': defRad, 'Nh': defRad, 'Fl': defRad, 'Mc': defRad,
    'Lv': defRad, 'Ts': defRad, 'Og': defRad
}
# Metallic radii from N.N. Greenwood; A. Earnshaw (1997) "Chemistry of Elements (2nd ed.)" Butterworth-Heinemann;
# Recommendations of values for multipliers: {radMult: 1.5, alphaMult: 2.5}
METALLIC_RAD_DICT = {
    'H': defRad, 'He': defRad, 'Li': 1.52, 'Be': 1.12, 'B': defRad, 'C': defRad, 'N': defRad, 'O': defRad, 'F': defRad,
    'Ne': defRad, 'Na': 1.86, 'Mg': 1.60, 'Al': 1.43, 'Si': defRad, 'P': defRad, 'S': defRad, 'Cl': defRad,
    'Ar': defRad, 'K': 2.27, 'Ca': 1.97, 'Sc': 1.62, 'Ti': 1.47, 'V': 1.34, 'Cr': 1.28, 'Mn': 1.27, 'Fe': 1.26,
    'Co': 1.25, 'Ni': 1.24, 'Cu': 1.28, 'Zn': 1.34, 'Ga': 1.35, 'Ge': defRad, 'As': defRad, 'Se': defRad, 'Br': defRad,
    'Kr': defRad, 'Rb': 2.48, 'Sr': 2.15, 'Y': 1.80, 'Zr': 1.60, 'Nb': 1.46, 'Mo': 1.39, 'Tc': 1.36, 'Ru': 1.34,
    'Rh': 1.34, 'Pd': 1.37, 'Ag': 1.44, 'Cd': 1.51, 'In': 1.67, 'Sn': defRad, 'Sb': defRad, 'Te': defRad, 'I': defRad,
    'Xe': defRad, 'Cs': 2.65, 'Ba': 2.22, 'La': 1.87, 'Ce': 1.818, 'Pr': 1.824, 'Nd': 1.814, 'Pm': 1.834, 'Sm': 1.804,
    'Eu': 1.804, 'Gd': 1.804, 'Tb': 1.773, 'Dy': 1.781, 'Ho': 1.762, 'Er': 1.761, 'Tm': 1.759, 'Yb': 1.76, 'Lu': 1.738,
    'Hf': 1.59, 'Ta': 1.46, 'W': 1.39, 'Re': 1.37, 'Os': 1.35, 'Ir': 1.355, 'Pt': 1.385, 'Au': 1.44, 'Hg': 1.51,
    'Tl': 1.70, 'Pb': defRad, 'Bi': defRad, 'Po': defRad, 'At': defRad, 'Rn': defRad, 'Fr': defRad, 'Ra': defRad,
    'Ac': defRad, 'Th': 1.79, 'Pa': 1.63, 'U': 1.56, 'Np': 1.55, 'Pu': 1.59, 'Am': 1.73, 'Cm': 1.74, 'Bk': 1.70,
    'Cf': 1.86, 'Es': 1.86, 'Fm': defRad, 'Md': defRad, 'No': defRad, 'Lr': defRad, 'Rf': defRad, 'Db': defRad,
    'Sg': defRad, 'Bh': defRad, 'Hs': defRad, 'Mt': defRad, 'Ds': defRad, 'Rg': defRad, 'Cn': defRad, 'Nh': defRad,
    'Fl': defRad, 'Mc': defRad, 'Lv': defRad, 'Ts': defRad, 'Og': defRad
}
PLT_PARAMS = {'paper': {'figSize': (3.5, 2.5), 'dpi': 300, 'fontSize': 'medium', 'labelSize': 'small',
                        'legendSize': 'x-small', 'lineWidth': 0.5, 'markerSize': 24},
              'notebook': {'figSize': (3.5, 2.5), 'dpi': 120, 'fontSize': 'medium', 'labelSize': 'small',
                         'legendSize': 'x-small', 'lineWidth': 0.5, 'markerSize': 18},
              'poster': {'figSize': (4.5, 3.5), 'dpi': 600, 'fontSize': 'x-large', 'labelSize': 'large',
                         'legendSize': 'medium', 'lineWidth': 1.0, 'markerSize': 48},
              'talk': {'figSize': (4, 3), 'dpi': 144, 'fontSize': 'large', 'labelSize': 'medium', 'legendSize': 'small',
                       'lineWidth': 1.0, 'markerSize': 36}}
