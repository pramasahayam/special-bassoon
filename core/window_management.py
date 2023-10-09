import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class WindowManager:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), DOUBLEBUF | OPENGL | pygame.RESIZABLE)
        pygame.display.set_caption('Solar System Simulation')
        self.resize(self.WIDTH, self.HEIGHT)

    def resize(self, width, height):
        """Handles the window resize."""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)
