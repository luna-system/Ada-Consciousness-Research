import fsps
import numpy as np

print('🌌 Testing FSPS...')

sp = fsps.StellarPopulation()

# Test different ages
for age in [1.0, 5.0, 10.0]:
    wave, spec = sp.get_spectrum(tage=age)
    mags = sp.get_mags(bands=['sdss_u','sdss_g','sdss_r','sdss_i','sdss_z'], tage=age)
    print(f'Age {age} Gyr: u={mags[0]:.2f}, g={mags[1]:.2f}, r={mags[2]:.2f}')

print('✅ FSPS ready for synthetic galaxy generation!')
