import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class WindowManager:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 960, 480
        self.resizable = True
        self.create_window()

    def create_window(self):
        """Create or recreate the window based on the current settings."""
        flags = DOUBLEBUF | OPENGL
        if self.resizable:
            flags |= pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags)
        pygame.display.set_caption('Solar System Simulation')
        self.resize(self.WIDTH, self.HEIGHT)

    def set_resizable(self, resizable):
        """Enable or disable window resizing."""
        if self.resizable != resizable:
            self.resizable = resizable
            self.create_window()

    def resize(self, width, height):
        """Handles the window resize."""
        self.WIDTH = width
        self.HEIGHT = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 600000.0)
        glMatrixMode(GL_MODELVIEW)

    def get_current_dimensions(self):
        return self.WIDTH, self.HEIGHT
