import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from core.user_interactions import UserInteractions

class SolarSystem:
    def __init__(self, space_bodies, screen):
        self.space_bodies = space_bodies
        self.screen = screen
        self.interactions = UserInteractions()
        self.selected_planet = None  # To keep track of the selected planet

    def draw_body(self, body, t, override_color=None):
        glColor3fv(override_color if override_color else body.color)
        quad = gluNewQuadric()
        slices, stacks = 100, 100
        glPushMatrix()
        x, y, z = body.compute_position(t)
        glTranslatef(x * 1000, y * 1000, z * 1000)  # Scaling factor for visualization
        gluSphere(quad, body.radius, slices, stacks)
        glPopMatrix()

    def pick_planet(self, mouse_pos, t):
        # Setting up off-screen render
        temp_buffer = glReadPixels(0, 0, self.screen.get_width(), self.screen.get_height(), GL_RGB, GL_UNSIGNED_BYTE)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for idx, body in enumerate(self.space_bodies):
            unique_color = (idx+1, 0, 0)  # Using the red channel for simplicity
            self.draw_body(body, t, override_color=unique_color)

        x, y = mouse_pos
        y = self.screen.get_height() - y  # Flip the y-coordinate
        color_under_mouse = glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        
        # Restore previous buffer
        glDrawPixels(self.screen.get_width(), self.screen.get_height(), GL_RGB, GL_UNSIGNED_BYTE, temp_buffer)

        planet_idx = color_under_mouse[0] - 1
        if 0 <= planet_idx < len(self.space_bodies):
            return self.space_bodies[planet_idx]
        else:
            return None

    def handle_event(self, event, resize, t):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected_planet = self.pick_planet(event.pos, t)
            if self.selected_planet:
                # Handle showing info box for the selected planet
                # This can be implemented further based on how you want to display the info
                print(f"Selected: {self.selected_planet.name}")
        self.interactions.handle_event(event, resize)

    def render(self, t):
        for body in self.space_bodies:
            self.draw_body(body, t)
