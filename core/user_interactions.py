import pygame
from OpenGL.GL import *

class UserInteractions:
    def __init__(self):
        # Zooming and panning parameters
        self.LINEAR_ZOOM_AMOUNT = 100.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -5000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE
        self.MIN_ZOOM_IN = -500
        self.MAX_ZOOM_OUT = -10000

    def handle_event(self, event, resize):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        self.dragging = True
                        self.last_mouse_x, self.last_mouse_y = event.pos
                    case 4:  # Zooming in
                        new_distance = self.CAMERA_DISTANCE + self.LINEAR_ZOOM_AMOUNT
                        if new_distance <= self.MIN_ZOOM_IN:
                            self.CAMERA_DISTANCE = new_distance
                            glTranslatef(0, 0, self.LINEAR_ZOOM_AMOUNT)
                    case 5:  # Zooming out
                        new_distance = self.CAMERA_DISTANCE - self.LINEAR_ZOOM_AMOUNT
                        if new_distance >= self.MAX_ZOOM_OUT:
                            self.CAMERA_DISTANCE = new_distance
                            glTranslatef(0, 0, -self.LINEAR_ZOOM_AMOUNT)
            case pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            case pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - self.last_mouse_x
                    dy = mouse_y - self.last_mouse_y
                    glTranslatef(dx * 0.5, -dy * 0.5, 0)
                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
