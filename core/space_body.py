from skyfield.api import load
import numpy as np

class SpaceBody:
    def __init__(self, radius, color, skyfield_name, data_url, speed_multiplier=1.0, orbital_center=None):
        self.radius = radius
        self.color = color
        self.skyfield_name = skyfield_name
        self.data_url = data_url
        self.speed_multiplier = speed_multiplier
        self.orbital_center = orbital_center
        
        self.ts = load.timescale()
        self.ephemeris = load(data_url)
        self.body = self.ephemeris[skyfield_name]

    def compute_position(self, t):
        """
        Compute the position using Skyfield.
        Returns x, y, z coordinates.
        """
        astrometric = self.body.at(t)
        ra, dec, dist = astrometric.radec()

        # Convert RA, Dec, Distance to Cartesian coordinates
        x = dist.au * np.cos(dec.radians) * np.cos(ra.radians)
        y = dist.au * np.cos(dec.radians) * np.sin(ra.radians)
        z = dist.au * np.sin(dec.radians)
        
        return x, y, z
