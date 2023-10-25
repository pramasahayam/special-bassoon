from skyfield.api import load
import pygame
from OpenGL.GL import glGenTextures, glBindTexture, glTexImage2D, GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, glTexParameterf, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR
import numpy as np

class SpaceBody:

    MIN_SIZE = 5  
    MAX_SUN_SIZE = 250  
    SMALLEST_RADIUS = 0.25  
    SUN_RADIUS = 100  

    BASE_SCALING_FACTOR = MAX_SUN_SIZE / SUN_RADIUS

    def __init__(self, radius, color, skyfield_name, data_url, 
                 orbital_center=None, name="", description="", orbital_period="", distance_from_sun="", 
                 mass="", diameter="", gravity="", avg_temperature="", orbit_distance="", texture_path=None):
        self.radius = radius
        self.color = color
        self.name = name
        self.mass = mass
        self.diameter = diameter
        self.avg_temperature = avg_temperature
        self.gravity = gravity
        self.description = description
        self.skyfield_name = skyfield_name
        self.data_url = data_url
        self.orbital_center = orbital_center
        self.orbital_period = orbital_period
        self.distance_from_sun = distance_from_sun
        self.orbit_distance = orbit_distance
        self.visual_radius = self.adjust_size_for_visibility(self.radius)

        self.texture_path = texture_path
        self.texture_id = None
        self.load_texture()
        
        self.ts = load.timescale()
        self.ephemeris = load(data_url)
        self.body = self.ephemeris[skyfield_name]

    def load_texture(self):
        print("loading textures...") # Debug
        if self.texture_path:
            texture_surface = pygame.image.load(self.texture_path)
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width, height = texture_surface.get_size()

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            
            # Set texture parameters
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def compute_position(self, t):
        """
        Compute the position using Skyfield and adjust for visualization.
        Returns x, y, z coordinates.
        """
        astrometric = self.body.at(t)
        ra, dec, dist = astrometric.radec()

        # Determine angle based on current position in orbit
        angle = self.get_orbit_angle(ra.radians)

        # Scale distance using a non-linear function
        scaled_distance = self.scale_distance(dist.au)
        
        # Calculate x, y coordinates
        x = scaled_distance * np.cos(angle)
        y = scaled_distance * np.sin(angle)
        
        # Vary z-coordinate based on actual distance
        z = self.get_height(dist.au)
        
        return x, y, z
    
    def adjust_size_for_visibility(self, size):
        """
        Adjust the size of celestial bodies for better visibility.
        """
        # Determine the scaling factor based on the size of the celestial body
        if size < SpaceBody.MIN_SIZE/2:
            scaling_factor = SpaceBody.BASE_SCALING_FACTOR * 20
        elif size < SpaceBody.MIN_SIZE:
            scaling_factor = SpaceBody.BASE_SCALING_FACTOR * 10
        elif size < SpaceBody.SUN_RADIUS / 2: # Mainly to not include the Sun itself
            scaling_factor = SpaceBody.BASE_SCALING_FACTOR * 7
        else:
            scaling_factor = SpaceBody.BASE_SCALING_FACTOR * 1.2
        
        adjusted_size = size * scaling_factor
        
        return adjusted_size

    def get_orbit_angle(self, ra):
        """
        Determine the angle based on the right ascension.
        """
        return ra

    def scale_distance(self, distance):
        """
        Scale the distance using a non-linear function.
        """
        return np.log(distance + 1)

    def get_height(self, distance):
        """
        Vary the z-coordinate based on the distance.
        """
        return distance / 10.0
