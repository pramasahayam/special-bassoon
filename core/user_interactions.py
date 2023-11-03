import pygame
from pygame.locals import *
from OpenGL.GL import *

class UserInteractions:
    def __init__(self, window_manager, imgui_manager, center_button):
        # Zooming and panning parameters
        self.imgui_manager = imgui_manager
        self.window_manager = window_manager
        self.center_button = center_button
        self.screen = self.window_manager.screen
        self.LINEAR_ZOOM_AMOUNT = 400.0
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
                        if self.center_button.mouse_on_button(event.pos):
                            self.center_button.handle_click()
                        else:
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
                    glTranslatef(dx * 3, -dy * 3, 0)
                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
                width, height = self.screen.get_size()
                dimensions = self.window_manager.get_current_dimensions()
                self.center_button.update_window_size(dimensions[0], dimensions[1])

                
            case pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # Check if the "w" key is pressed
                    self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE
                    glLoadIdentity()  # Reset the modelview matrix to identity
                    glTranslatef(0, 0, self.CAMERA_DISTANCE)                
