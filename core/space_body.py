from skyfield.api import load
import pygame
from OpenGL.GL import glGenTextures, glBindTexture, glTexImage2D, GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, glTexParameterf, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR
import numpy as np

class SpaceBody:  

    BASE_SCALING_FACTOR = 2.5

    def __init__(self, radius, skyfield_name, data_url, 
                 orbital_center=None, name="", description="", orbital_period="", distance_from_sun="", 
                 mass="", diameter="", gravity="", avg_temperature="", day="",year="",AU="", orbit_distance="",
                texture_path=None):
        self.radius = radius
        self.name = name
        self.mass = mass
        self.diameter = diameter
        self.avg_temperature = avg_temperature
        self.gravity = gravity
        self.day = day
        self.year = year
        self.description = description
        self.AU = AU
        self.skyfield_name = skyfield_name
        self.data_url = data_url
        self.orbital_center = orbital_center
        self.orbital_period = orbital_period
        self.distance_from_sun = distance_from_sun
        self.orbit_distance = orbit_distance

        self.texture_path = texture_path
        self.texture_id = None
        self.load_texture()
        
        self.ts = load.timescale()
        self.ephemeris = load(data_url)
        self.body = self.ephemeris[skyfield_name]

    def load_texture(self):
        if self.texture_path:
            print(f"Loading Texture: {self.texture_path}") # Debug
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
        Compute the position using Skyfield ephemeris data.
        Returns x, y, z coordinates in astronomical units (au).
        """
        astrometric = self.body.at(t)
        x, y, z = astrometric.position.au
    
        if self.orbital_center:
            return -x*1.005, -y*1.005, z*1.005
        else:
            return -x, -y, z


    