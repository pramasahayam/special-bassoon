import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from core.user_interactions import UserInteractions
from core.window_management import WindowManager
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

class SolarSystem:
    def __init__(self):
        self.window = WindowManager()
        self.interactions = UserInteractions(self.window.screen)
        self.clicked_mouse_position = None
        
        # List of space bodies in our solar system
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto()
        ]

        self.selected_planet = None
        self.infobox_visible = False


    def handle_event(self, event, t):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.infobox_visible:
                self.infobox_visible = False
                self.selected_planet = None
                self.clicked_mouse_position = None  # Reset the stored mouse position
            else:
                clicked_planet = self.pick_planet(event.pos, t)
                if clicked_planet:
                    self.selected_planet = clicked_planet
                    self.infobox_visible = True
                    self.clicked_mouse_position = event.pos  # Store the mouse position
                    print(f"Clicked on: {self.selected_planet.name}")  # Debugging


    def world_to_screen(self, x, y, z):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        screen_x, screen_y, screen_z = gluProject(x, y, z, modelview, projection, viewport)
        return screen_x, self.window.HEIGHT - screen_y  # Flip the y-coordinate because of different coordinate systems


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
            return self.space_bodies[planet_idx]
        return None

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

    def render_ui(self):
        if self.infobox_visible and self.selected_planet and self.clicked_mouse_position:
            # Use the stored mouse position
            mouse_x, mouse_y = self.clicked_mouse_position
            
            # Offset the position diagonally to the left (and a bit up)
            offset_x = -300  
            offset_y = -150   
            infobox_x = mouse_x + offset_x
            infobox_y = mouse_y + offset_y
            
            # Set the position of the ImGui window using the offset position
            imgui.set_next_window_position(infobox_x, infobox_y)
            
            # Define the window flags
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE
            
            # Use ImGui to render the info box for the selected planet with the flags
            imgui.begin("Info Box", self.infobox_visible, flags)
            imgui.text(f"Name: {self.selected_planet.name}")
            imgui.text(f"Description: {self.selected_planet.description}")
            imgui.text(f"Radius: {self.selected_planet.radius}")
            imgui.text(f"Orbital Period: {self.selected_planet.orbital_period}")
            imgui.end()







