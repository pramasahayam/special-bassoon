import pygame
from pygame.locals import *
from OpenGL.GL import *

class UserInteractions:
    def __init__(self, window_manager, gui_manager):
        # Zooming and panning parameters
        self.gui_manager = gui_manager
        self.window_manager = window_manager
        self.skybox_tenth_size = 300000/10 # Same size as in solar_system.py
        self.LINEAR_ZOOM_AMOUNT = 400.0
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
        
    def handle_event(self, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            case pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)
            case pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            case pygame.VIDEORESIZE:
                self.handle_resize(event)

    def handle_mouse_button_down(self, event):
        match event.button:
            case 1:
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
            case 4:  # Zooming in
                self.zoom_in()
            case 5:  # Zooming out
                self.zoom_out()

    def handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False

    def handle_mouse_motion(self, event):
        if self.dragging:
            self.drag_camera(event)

    def handle_resize(self, event):
        width, height = event.size
        self.window_manager.resize(width, height)
        self.gui_manager.handle_resize(width, height)

    def zoom_in(self):
        new_distance = self.CAMERA_DISTANCE + self.LINEAR_ZOOM_AMOUNT
        if new_distance <= self.MIN_ZOOM_IN:
            self.CAMERA_DISTANCE = new_distance
            glTranslatef(0, 0, self.LINEAR_ZOOM_AMOUNT)

    def zoom_out(self):
        new_distance = self.CAMERA_DISTANCE - self.LINEAR_ZOOM_AMOUNT
        if new_distance >= self.MAX_ZOOM_OUT:
            self.CAMERA_DISTANCE = new_distance
            glTranslatef(0, 0, -self.LINEAR_ZOOM_AMOUNT)

    def drag_camera(self, event):
        mouse_x, mouse_y = event.pos
        dx = mouse_x - self.last_mouse_x
        dy = mouse_y - self.last_mouse_y

        new_camera_x = self.camera_position[0] + dx * 15
        new_camera_y = self.camera_position[1] - dy * 15
        new_camera_x = max(min(new_camera_x, self.camera_limits['right']), self.camera_limits['left'])
        new_camera_y = max(min(new_camera_y, self.camera_limits['up']), self.camera_limits['down'])

        glTranslatef(new_camera_x - self.camera_position[0], new_camera_y - self.camera_position[1], 0)
        self.camera_position[0] = new_camera_x
        self.camera_position[1] = new_camera_y

        self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

    def focus_on_body(self, solar_system, body_position, body_radius):
        # Calculate the ring radius and the desired distance based on the celestial body's size
        ring_radius = solar_system.get_ring_radius(body_radius)
        desired_distance = -(ring_radius * 2)

        # Calculate camera position to center on the celestial body
        new_camera_x = -body_position[0]
        new_camera_y = -body_position[1]
        new_camera_z = desired_distance if body_position[2] == 0 else -body_position[2]

        glLoadIdentity()
        glTranslatef(new_camera_x, new_camera_y, new_camera_z-ring_radius)
        self.camera_position = [new_camera_x, new_camera_y, new_camera_z-ring_radius]

        # Update the last known mouse position to prevent jumping when starting to pan again
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

        print(f"Camera repositioned to: x={new_camera_x}, \t y={new_camera_y}, \t z={new_camera_z}")
        z_value = new_camera_z-ring_radius
        self.gui_manager.zoom = ((z_value + 50000)/60000) * 100


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
        
    def zoom_slider(self, camera_value):
        glLoadIdentity()
        camera_x = self.camera_position[0]
        camera_y = self.camera_position[1]
        glTranslatef(camera_x, camera_y, camera_value)
        # Update the internal camera position state
        self.camera_position = [camera_x, camera_y, camera_value]