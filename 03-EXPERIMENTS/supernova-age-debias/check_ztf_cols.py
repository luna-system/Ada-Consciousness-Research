import pandas as pd

sne = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv')
print('ZTF columns:', sne.columns.tolist())
