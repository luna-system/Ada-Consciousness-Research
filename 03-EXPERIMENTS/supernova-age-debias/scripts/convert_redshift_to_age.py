"""
Redshift to Age Converter for Cosmological Analysis

Converts observed redshifts to stellar population ages using cosmological
lookback time calculations. This allows us to use SDSS redshifts as a
proxy for galaxy ages in our training data.

The conversion uses:
- Lookback time: how long ago the light was emitted
- Age of universe at redshift z: t(z) = t_0 - lookback(z)
- Stellar population age is typically younger than universe age at that z

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedshiftToAgeConverter:
    """
    Convert redshifts to stellar population ages using cosmology.
    """
    
    def __init__(
        self,
        H0: float = 67.4,  # km/s/Mpc (Planck 2018)
        Om0: float = 0.315,  # Matter density (Planck 2018)
        Ode0: float = 0.685,  # Dark energy density
    ):
        """
        Initialize with cosmological parameters.
        
        Args:
            H0: Hubble constant in km/s/Mpc
            Om0: Matter density parameter
            Ode0: Dark energy density parameter
        """
        self.cosmo = FlatLambdaCDM(H0=H0, Om0=Om0, Tcmb0=2.725)
        self.age_universe = self.cosmo.age(0).to(u.Gyr).value  # Current age
        
        logger.info(f"🌌 Cosmology initialized:")
        logger.info(f"   H0 = {H0} km/s/Mpc")
        logger.info(f"   Ωm = {Om0}")
        logger.info(f"   ΩΛ = {Ode0}")
        logger.info(f"   Age of universe = {self.age_universe:.2f} Gyr")
    
    def redshift_to_lookback(self, z: float) -> float:
        """
        Convert redshift to lookback time in Gyr.
        
        Lookback time = how long ago the light was emitted.
        
        Args:
            z: Redshift
            
        Returns:
            Lookback time in Gyr
        """
        return self.cosmo.lookback_time(z).to(u.Gyr).value
    
    def redshift_to_universe_age(self, z: float) -> float:
        """
        Convert redshift to age of universe at that redshift.
        
        Age at z = current age - lookback time
        
        Args:
            z: Redshift
            
        Returns:
            Age of universe at redshift z in Gyr
        """
        return self.cosmo.age(z).to(u.Gyr).value
    
    def redshift_to_stellar_age(
        self,
        z: float,
        formation_redshift: float = 10.0,
        mass_weighted: bool = True,
    ) -> float:
        """
        Estimate stellar population age from redshift.
        
        This is a simplified model. Real stellar population ages depend on:
        - Star formation history
        - Formation redshift
        - Mass-weighted vs luminosity-weighted age
        
        Args:
            z: Observed redshift
            formation_redshift: When stars formed (default z=10)
            mass_weighted: Whether to use mass-weighted age
            
        Returns:
            Estimated stellar population age in Gyr
        """
        # Age of universe at observed redshift
        age_at_z = self.redshift_to_universe_age(z)
        
        # Age of universe at formation
        age_at_formation = self.redshift_to_universe_age(formation_redshift)
        
        # Maximum possible age (if all stars formed at formation_redshift)
        max_age = age_at_z - age_at_formation
        
        # For mass-weighted age, typically younger than max
        # (star formation continues over time)
        if mass_weighted:
            # Simple model: mass-weighted age is ~70% of max age
            # This accounts for ongoing star formation
            stellar_age = max_age * 0.7
        else:
            # Luminosity-weighted age is typically younger
            stellar_age = max_age * 0.5
        
        return max(stellar_age, 0.1)  # Minimum 0.1 Gyr
    
    def convert_catalog(
        self,
        catalog_file: str = "data/matched_catalog_real.csv",
        output_file: str = "data/matched_catalog_with_ages.csv",
        formation_redshift: float = 10.0,
    ) -> pd.DataFrame:
        """
        Convert redshifts to ages for entire catalog.
        
        Args:
            catalog_file: Path to matched catalog with redshifts
            output_file: Path to save catalog with ages
            formation_redshift: Assumed formation redshift
            
        Returns:
            DataFrame with added age columns
        """
        logger.info("🌌 Converting redshifts to stellar population ages...")
        
        # Load catalog
        catalog = pd.read_csv(catalog_file)
        logger.info(f"   Loaded {len(catalog)} galaxies")
        
        # Calculate ages
        catalog['lookback_time'] = catalog['zHD'].apply(self.redshift_to_lookback)
        catalog['universe_age_at_z'] = catalog['zHD'].apply(self.redshift_to_universe_age)
        catalog['stellar_age_max'] = catalog['universe_age_at_z'] - self.redshift_to_universe_age(formation_redshift)
        catalog['stellar_age_estimated'] = catalog['zHD'].apply(
            lambda z: self.redshift_to_stellar_age(z, formation_redshift)
        )
        
        # Add age uncertainty (rough estimate)
        catalog['stellar_age_err'] = catalog['stellar_age_estimated'] * 0.3  # 30% uncertainty
        
        # Save
        catalog.to_csv(output_file, index=False)
        logger.info(f"💾 Saved to {output_file}")
        
        # Summary
        logger.info(f"\n📊 Age Conversion Summary:")
        logger.info(f"   Age range: {catalog['stellar_age_estimated'].min():.2f} - {catalog['stellar_age_estimated'].max():.2f} Gyr")
        logger.info(f"   Mean age: {catalog['stellar_age_estimated'].mean():.2f} Gyr")
        logger.info(f"   Lookback range: {catalog['lookback_time'].min():.2f} - {catalog['lookback_time'].max():.2f} Gyr")
        
        return catalog
    
    def compare_cosmologies(
        self,
        z_range: np.ndarray = None,
        H0_values: list = [67.4, 70.0, 73.0],
        Om0_values: list = [0.27, 0.315, 0.35],
    ) -> pd.DataFrame:
        """
        Compare age estimates for different cosmological parameters.
        
        Useful for understanding systematic uncertainty from cosmology choice.
        """
        if z_range is None:
            z_range = np.linspace(0.01, 1.0, 100)
        
        results = []
        
        for H0 in H0_values:
            for Om0 in Om0_values:
                cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)
                
                for z in z_range:
                    age = cosmo.age(z).to(u.Gyr).value
                    lookback = cosmo.lookback_time(z).to(u.Gyr).value
                    
                    results.append({
                        'H0': H0,
                        'Om0': Om0,
                        'z': z,
                        'age': age,
                        'lookback': lookback,
                    })
        
        return pd.DataFrame(results)


def main():
    """Main conversion pipeline."""
    logger.info("🌌 Redshift to Age Conversion")
    logger.info("=" * 60)
    
    Path("data").mkdir(exist_ok=True)
    
    # Initialize converter
    converter = RedshiftToAgeConverter()
    
    # Convert catalog
    catalog = converter.convert_catalog()
    
    logger.info("=" * 60)
    logger.info("✅ Conversion complete!")
    logger.info("🍩 'Real ages for real cosmology!'")
    
    return 0


if __name__ == "__main__":
    exit(main())
