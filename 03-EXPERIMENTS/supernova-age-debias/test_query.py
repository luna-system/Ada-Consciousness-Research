#!/usr/bin/env python3
"""Test SDSS query API."""

from astroquery.sdss import SDSS
import inspect

print("query_region signature:")
print(inspect.signature(SDSS.query_region))
print()

print("query_crossid signature:")
print(inspect.signature(SDSS.query_crossid))
print()

# Try to see what parameters are accepted
print("Trying simple query...")
from astropy import coordinates as coords
import astropy.units as u

pos = coords.SkyCoord(ra=167.62646*u.deg, dec=55.16983*u.deg, frame='icrs')

try:
    result = SDSS.query_crossid(pos, radius=3*u.arcsec)
    print(f"crossid success: {result}")
except Exception as e:
    print(f"crossid error: {e}")

try:
    result = SDSS.query_region(pos, radius=3*u.arcsec)
    print(f"region success: {result}")
except Exception as e:
    print(f"region error: {e}")
