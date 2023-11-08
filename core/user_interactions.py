import pygame
from pygame.locals import *
from OpenGL.GL import *

class UserInteractions:
    def __init__(self, window_manager, gui_manager):
        # Zooming and panning parameters
        self.gui_manager = gui_manager
        self.window_manager = window_manager
        self.screen = self.window_manager.screen
        self.skybox_tenth_size = 300000/10 # Same size as in solar_system.py
        self.LINEAR_ZOOM_AMOUNT = 50.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -15000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE

        self.MIN_ZOOM_IN = 10000
        self.MAX_ZOOM_OUT = -50000

        # Camera position limits
        self.camera_limits = {
            'left': -self.skybox_tenth_size,
            'right': self.skybox_tenth_size,
            'up': self.skybox_tenth_size,
            'down': -self.skybox_tenth_size,
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

    def focus_on_body(self, solar_system, body_position, body_radius):
        # Calculate the ring radius and the desired distance based on the celestial body's size and a FOV factor
        ring_radius = solar_system.get_ring_radius(body_radius)
        desired_distance = -(ring_radius * 2)

        # Calculate camera position to center on the celestial body
        new_camera_x = -body_position[0]
        new_camera_y = -body_position[1]
        new_camera_z = desired_distance if body_position[2] == 0 else -body_position[2]

        # You could add a transition effect here to move from the current camera position to the new position smoothly
        # For now, we set the position directly
        glLoadIdentity()

        
        glTranslatef(new_camera_x, new_camera_y, new_camera_z-ring_radius)
        self.camera_position = [new_camera_x, new_camera_y, new_camera_z-ring_radius]

        print(f"Camera repositioned to: x={new_camera_x}, \t y={new_camera_y}, \t z={new_camera_z}")

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