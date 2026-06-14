from astroquery.sdss import SDSS
from astropy import coordinates as coords
import astropy.units as u

# Query a small region around a Pantheon+ host
pos = coords.SkyCoord('167.62646d 55.16983d', frame='icrs')
print('Querying SDSS for galaxies near Pantheon+ host...')
xid = SDSS.query_region(pos, radius=2*u.arcmin, spectro=True)
print(f'Found {len(xid)} spectra' if xid is not None else 'No spectra found')
if xid is not None:
    print(xid.colnames[:10])
    print(f'Total columns: {len(xid.colnames)}')
