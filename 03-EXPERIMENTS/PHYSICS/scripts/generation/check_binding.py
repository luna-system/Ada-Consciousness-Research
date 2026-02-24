# Correct total electron binding energies (approximate, in eV)
# These are the energy required to remove ALL electrons from the atom

BINDING_ENERGIES = {
    1: ('H', 'Hydrogen', 13.6),
    2: ('He', 'Helium', 79.0),
    3: ('Li', 'Lithium', 203.5),
    4: ('Be', 'Beryllium', 399.0),
    5: ('B', 'Boron', 667.0),
    6: ('C', 'Carbon', 1030.0),
    7: ('N', 'Nitrogen', 1485.0),  # ~1485 eV
    8: ('O', 'Oxygen', 2045.0),     # ~2045 eV  
    9: ('F', 'Fluorine', 2680.0),
    10: ('Ne', 'Neon', 3360.0),
    11: ('Na', 'Sodium', 4110.0),
    12: ('Mg', 'Magnesium', 4935.0),
    13: ('Al', 'Aluminum', 5820.0),
    14: ('Si', 'Silicon', 6770.0),
    15: ('P', 'Phosphorus', 7780.0),
    16: ('S', 'Sulfur', 8850.0),
    17: ('Cl', 'Chlorine', 9970.0),
    18: ('Ar', 'Argon', 11150.0),
    26: ('Fe', 'Iron', 41150.0),
    29: ('Cu', 'Copper', 45800.0),
}

print("Total Electron Binding Energies:")
print("-" * 50)
for z, (sym, name, be) in BINDING_ENERGIES.items():
    print(f"{sym:2s} ({z:2d}): {be:8.1f} eV - {name}")
