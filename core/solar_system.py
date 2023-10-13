import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from core.user_interactions import UserInteractions
from core.window_management import WindowManager
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

class SolarSystem:
    def __init__(self):
        self.window = WindowManager()
        self.interactions = UserInteractions(self.window.screen)
        
        # List of space bodies in our solar system
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto()
        ]

        self.selected_planet = None

    def handle_event(self, event, t):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected_planet = self.pick_planet(event.pos, t)
            if self.selected_planet:
                print(f"Clicked on: {self.selected_planet.name}") # Debugging


    def pick_planet(self, mouse_pos, t):
        # Render each body with a unique color for picking
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for idx, body in enumerate(self.space_bodies):
            unique_color = (idx+1, 0, 0)
            self.draw_body(body, t, unique_color)
        
        x, y = mouse_pos
        y = self.window.screen.get_height() - y
        color_under_mouse = glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)

        print(f"Color under mouse: {color_under_mouse}")  # Debugging

        # Convert the color back to an index
        planet_idx = int(color_under_mouse[0]) - 1

        print(f"Calculated planet index: {planet_idx}")  # Debugging

        if 0 <= planet_idx < len(self.space_bodies):
            print(f"Planet index detected: {planet_idx}")  # Debugging
            return self.space_bodies[planet_idx]
        print("No planet detected for the given color.")  # Debugging
        return None

    def render_ui(self):
        if self.selected_planet:
            self.interactions.show_info_box(self.selected_planet)

    def draw_body(self, body, t, color=None):
        if color is None:
            glColor3fv(body.color)
        else:
            glColor3fv((color[0]/255.0, color[1]/255.0, color[2]/255.0))
        
        quad = gluNewQuadric()
        glPushMatrix()
        x, y, z = body.compute_position(t)
        glTranslatef(x * 1000, y * 1000, z * 1000)  # Scaling factor for visualization
        gluSphere(quad, body.radius, 100, 100)
        glPopMatrix()
