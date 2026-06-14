import numpy as np
import pandas as pd

# Load samples
samples = ['full', 'young', 'old']

results = []

for sample in samples:
    try:
        lcdm = np.load(f'data/mcmc/{sample}/samples_lcdm.npy')
        nonaccel = np.load(f'data/mcmc/{sample}/samples_nonaccel.npy')
        
        # Parameter medians
        lcdm_medians = np.median(lcdm, axis=0)
        nonaccel_medians = np.median(nonaccel, axis=0)
        
        # Parameter stds
        lcdm_stds = np.std(lcdm, axis=0)
        nonaccel_stds = np.std(nonaccel, axis=0)
        
        print(f"\n{'='*70}")
        print(f"📊 MCMC Results: {sample.upper()} Sample")
        print(f"{'='*70}")
        print(f"ΛCDM samples: {len(lcdm)}")
        print(f"Non-Accel samples: {len(nonaccel)}")
        
        print(f"\nΛCDM parameters (median ± std):")
        print(f"  H0 = {lcdm_medians[0]:.2f} ± {lcdm_stds[0]:.2f}")
        print(f"  Ωm = {lcdm_medians[1]:.3f} ± {lcdm_stds[1]:.3f}")
        print(f"  ΩΛ = {lcdm_medians[2]:.3f} ± {lcdm_stds[2]:.3f}")
        print(f"  M = {lcdm_medians[3]:.3f} ± {lcdm_stds[3]:.3f}")
        
        print(f"\nNon-Accel parameters (median ± std):")
        print(f"  H0 = {nonaccel_medians[0]:.2f} ± {nonaccel_stds[0]:.2f}")
        print(f"  q0 = {nonaccel_medians[1]:.3f} ± {nonaccel_stds[1]:.3f}")
        print(f"  M = {nonaccel_medians[2]:.3f} ± {nonaccel_stds[2]:.3f}")
        
        # Approximate BIC from best-fit log likelihood
        # (We'd need the actual log likelihood values, but we can approximate)
        
        results.append({
            'sample': sample,
            'lcdm_H0': lcdm_medians[0],
            'lcdm_H0_std': lcdm_stds[0],
            'lcdm_Om': lcdm_medians[1],
            'lcdm_OL': lcdm_medians[2],
            'lcdm_M': lcdm_medians[3],
            'nonaccel_H0': nonaccel_medians[0],
            'nonaccel_H0_std': nonaccel_stds[0],
            'nonaccel_q0': nonaccel_medians[1],
            'nonaccel_q0_std': nonaccel_stds[1],
            'nonaccel_M': nonaccel_medians[2],
            'nonaccel_M_std': nonaccel_stds[2],
        })
        
    except Exception as e:
        print(f"Error loading {sample}: {e}")

# Save results
df = pd.DataFrame(results)
df.to_csv('data/mcmc_parameter_summary.csv', index=False)
print(f"\n💾 Results saved to data/mcmc_parameter_summary.csv")
