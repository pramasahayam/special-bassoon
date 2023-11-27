from skyfield.api import load
import numpy as np

class SpaceBody:
    def __init__(self, radius, color, skyfield_name, data_url, mu="", orbital_center_mu="", semimajoraxis="",
                 orbital_center=None, name="", description="", orbital_period="", distance_from_sun="", 
                 mass="", diameter="", gravity="", avg_temperature="", age="", orbit_distance=""):
        self.radius = radius
        self.color = color
        self.name = name
        self.mass = mass
        self.diameter = diameter
        self.avg_temperature = avg_temperature
        self.gravity = gravity
        self.description = description
        self.age = age
        self.skyfield_name = skyfield_name
        self.data_url = data_url
        self.orbital_center = orbital_center
        self.orbital_period = orbital_period
        self.distance_from_sun = distance_from_sun
        self.orbit_distance = orbit_distance
        self.mu = mu
        self.orbital_center_mu = orbital_center_mu
        self.semimajoraxis = semimajoraxis
        
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
