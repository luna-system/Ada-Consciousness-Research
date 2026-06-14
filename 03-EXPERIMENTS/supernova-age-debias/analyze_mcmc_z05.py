import numpy as np
import pandas as pd

samples = ['full', 'young', 'old']
results = []

for sample in samples:
    lcdm = np.load(f'data/mcmc_z05/{sample}/samples_lcdm.npy')
    nonaccel = np.load(f'data/mcmc_z05/{sample}/samples_nonaccel.npy')
    
    lcdm_medians = np.median(lcdm, axis=0)
    nonaccel_medians = np.median(nonaccel, axis=0)
    lcdm_stds = np.std(lcdm, axis=0)
    nonaccel_stds = np.std(nonaccel, axis=0)
    
    print(f'\n{sample.upper()} SAMPLE (z > 0.05):')
    print(f'  LCDM: H0={lcdm_medians[0]:.2f}±{lcdm_stds[0]:.2f}, Om={lcdm_medians[1]:.3f}±{lcdm_stds[1]:.3f}, OL={lcdm_medians[2]:.3f}±{lcdm_stds[2]:.3f}, M={lcdm_medians[3]:.3f}±{lcdm_stds[3]:.3f}')
    print(f'  Non-Accel: H0={nonaccel_medians[0]:.2f}±{nonaccel_stds[0]:.2f}, q0={nonaccel_medians[1]:.3f}±{nonaccel_stds[1]:.3f}, M={nonaccel_medians[2]:.3f}±{nonaccel_stds[2]:.3f}')
    
    results.append({
        'sample': sample,
        'lcdm_H0': lcdm_medians[0],
        'lcdm_Om': lcdm_medians[1],
        'lcdm_OL': lcdm_medians[2],
        'lcdm_M': lcdm_medians[3],
        'nonaccel_H0': nonaccel_medians[0],
        'nonaccel_q0': nonaccel_medians[1],
        'nonaccel_M': nonaccel_medians[2],
    })

df = pd.DataFrame(results)
df.to_csv('data/mcmc_z05_parameter_summary.csv', index=False)
print('\n💾 Saved to data/mcmc_z05_parameter_summary.csv')
