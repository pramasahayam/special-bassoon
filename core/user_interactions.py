import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *

class UserInteractions:
    def __init__(self, window_manager, gui_manager):
        # Zooming and panning parameters
        self.gui_manager = gui_manager
        self.window_manager = window_manager
        self.screen = self.window_manager.screen
        self.skybox_eigth_size = 300000/10 # Same size as in solar_system.py
        self.LINEAR_ZOOM_AMOUNT = 450.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -15000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE

        self.MIN_ZOOM_IN = 400
        self.MAX_ZOOM_OUT = -50000

        # Camera position limits
        self.camera_limits = {
            'left': -self.skybox_eigth_size,
            'right': self.skybox_eigth_size,
            'up': self.skybox_eigth_size,
            'down': -self.skybox_eigth_size,
            'forward': self.MIN_ZOOM_IN,
            'backward': self.MAX_ZOOM_OUT
        }

        self.camera_position = [0, 0, self.CAMERA_DISTANCE]
        
    def handle_event(self, event, resize):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        self.dragging = True
                        self.last_mouse_x, self.last_mouse_y = event.pos
                    case 4:  # Zooming in
                        new_distance = self.CAMERA_DISTANCE + self.LINEAR_ZOOM_AMOUNT
                        # Ensure the new distance does not exceed the minimum zoom in limit
                        if new_distance < self.MIN_ZOOM_IN:
                            self.CAMERA_DISTANCE = new_distance
                            glTranslatef(0, 0, self.LINEAR_ZOOM_AMOUNT)

                    case 5:  # Zooming out
                        new_distance = self.CAMERA_DISTANCE - self.LINEAR_ZOOM_AMOUNT
                        # Ensure the new distance does not exceed the maximum zoom out limit
                        if new_distance > self.MAX_ZOOM_OUT:
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

                    # Calculate the new camera position
                    new_camera_x = self.camera_position[0] + dx * 15
                    new_camera_y = self.camera_position[1] - dy * 15

                    # Clamp the camera position to the defined limits
                    new_camera_x = max(min(new_camera_x, self.camera_limits['right']), self.camera_limits['left'])
                    new_camera_y = max(min(new_camera_y, self.camera_limits['up']), self.camera_limits['down'])

                    # Update the camera position
                    glTranslatef(new_camera_x - self.camera_position[0], new_camera_y - self.camera_position[1], 0)
                    self.camera_position[0] = new_camera_x
                    self.camera_position[1] = new_camera_y

                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
                self.gui_manager.handle_resize(width, height)

    def move_camera_to_body(self, body_position, body_radius):
        # Calculate the target position for the camera
        target_position = [body_position[0] * -1500, body_position[1] * -1500, body_position[2] * 1500]

        camera_offset = body_radius * 10

        new_camera_distance = -np.sqrt(target_position[0]**2 + target_position[1]**2 + (target_position[2] + camera_offset)**2)

        self.camera_position = [target_position[0], target_position[1], new_camera_distance]

        # Move the camera to the target position
        glLoadIdentity()
        glTranslatef(self.camera_position[0], self.camera_position[1], self.camera_position[2])

        # Update the CAMERA_DISTANCE to reflect the new position
        self.CAMERA_DISTANCE = new_camera_distance

        # Ensure the new distance respects the zoom limits
        self.CAMERA_DISTANCE = max(min(self.CAMERA_DISTANCE, self.MIN_ZOOM_IN), self.MAX_ZOOM_OUT)

    def get_camera_position(self):
        modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_position = [-modelview_matrix[3][i] for i in range(3)]
        return camera_position
    
    def get_camera_distance(self):
        return self.CAMERA_DISTANCE
    
    def center_camera(self):
        glLoadIdentity()
        glTranslatef(0, 0, self.CAMERA_DISTANCE)
        # Update the internal camera position state
        self.camera_position = [0, 0, self.CAMERA_DISTANCE]

    def set_camera_distance(self, distance):
        self.CAMERA_DISTANCE = distance
