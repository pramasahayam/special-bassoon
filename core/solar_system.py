import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from core.user_interactions import UserInteractions
from core.window_management import WindowManager
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Europa, Titan, Deimos, Phobos, Callisto, Io, Iapetus, Rhea, Oberon, Titania, Umbriel, Ariel

class SolarSystem:
    def __init__(self, imgui_manager=None):
        self.imgui_manager = imgui_manager
        self.window = WindowManager()
        self.interactions = UserInteractions(self.window, self.imgui_manager)
        self.clicked_mouse_position = None
        
        # List of space bodies in our solar system
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto(), Moon(), Europa(), Titan(), Deimos(),
            Phobos(), Callisto(), Io(), Iapetus(), 
            Rhea(), Oberon(), Titania(), Umbriel(), Ariel()
        ]

        self.selected_planet = None
        self.infobox_visible = False

    def handle_event(self, event, t):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        # If the infobox is visible, hide it
                        if self.infobox_visible:
                            self.infobox_visible = False
                            self.selected_planet = None
                            self.clicked_mouse_position = None  # Reset the stored mouse position

            case pygame.MOUSEBUTTONUP:
                match event.button:
                    case 1:
                        if self.interactions.dragging:
                            self.interactions.dragging = False
                            return

                        clicked_planet = self.pick_planet(event.pos, t)

                        if clicked_planet:
                            # If the user clicked on the same planet as before, do nothing
                            if clicked_planet == self.selected_planet:
                                return

                            # If the user clicked on a different planet, update the selected planet
                            self.selected_planet = clicked_planet
                            self.infobox_visible = True
                            self.clicked_mouse_position = event.pos  # Store the mouse position
                            print(f"Clicked on: {self.selected_planet.name}")  # Debug

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
        _, current_height = self.window.get_current_dimensions()
        y = current_height - y

        color_under_mouse = glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)

        # Convert the color back to an index
        planet_idx = int(color_under_mouse[0]) - 1

        print(f"Planet index: {planet_idx}")  # Debug

        if 0 <= planet_idx < len(self.space_bodies):
            return self.space_bodies[planet_idx]
        return None

    def draw_body(self, body, t, color=None):
        if color is None:
            glColor3fv(body.color)
        else:
            glColor3fv((color[0]/255.0, color[1]/255.0, color[2]/255.0))
        
        quad = gluNewQuadric()

        # If the body has a texture, bind it
        if body.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, body.texture_id)
            gluQuadricTexture(quad, GL_TRUE)
        else:
            glDisable(GL_TEXTURE_2D)

        glPushMatrix()
        x, y, z = body.compute_position(t)
        glTranslatef(x * 1000, y * 1000, z * 1000)  # Scaling factor for visualization
        gluSphere(quad, body.visual_radius, 100, 100)
        glPopMatrix()

    def render_ui(self):
        t = self.space_bodies[0].ts.now()

        if self.infobox_visible and self.selected_planet and self.clicked_mouse_position:
            mouse_x, mouse_y = self.clicked_mouse_position
            
            # Adjust the mouse position based on the window dimensions
            # _, current_height = self.window.get_current_dimensions()
            
            offset_x = -350 
            offset_y = -150   
            infobox_x = mouse_x + offset_x
            infobox_y = mouse_y + offset_y
            
            text_height = imgui.get_text_line_height()
            separator_height = imgui.get_frame_height_with_spacing()
            
            # List of attributes to display with their labels
            attributes = [
                ("Name", self.selected_planet.name),
                ("Description", self.selected_planet.description),
                ("Diameter", self.selected_planet.diameter),
                ("Mass", self.selected_planet.mass),
                ("Gravitational Acceleration", self.selected_planet.gravity),
                ("Average Temperature", self.selected_planet.avg_temperature),
                ("Distance to Earth", self.selected_planet.AU),
                ("Orbit Distance", self.selected_planet.orbit_distance),
                ("Day",self.selected_planet.day),
                ("Year",self.selected_planet.year),
                ("Coordinates", self.selected_planet.compute_position(t))
            ]

            total_height = sum(text_height for _, value in attributes if value)

            total_height += separator_height * (len([value for _, value in attributes if value]) - 1)

            if self.selected_planet.description:
                description_width = 280
                total_height += imgui.calc_text_size(f"Description: {self.selected_planet.description}", wrap_width=description_width)[1] - text_height

            # Add padding to the total height
            padding = 10  # Adjust as needed
            total_height += 2 * padding
            
            # Calculate the maximum width based on the longest attribute
            max_width = max(imgui.calc_text_size(f"{label}: {value}")[0] for label, value in attributes if value)
            infobox_width = max(300, max_width + 20)  # 20 is for some padding on the sides

            # Set the position and size of the ImGui window
            imgui.set_next_window_position(infobox_x, infobox_y)
            imgui.set_next_window_size(300, total_height)
            
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
        
            imgui.begin("Info Box", self.infobox_visible, flags)

            imgui.set_cursor_pos((imgui.get_cursor_pos()[0], imgui.get_cursor_pos()[1] + padding))  # Add top padding
        
            for i, (label, value) in enumerate(attributes):
                if value: 
                    if label == "Name":
                        # Bold and center the name
                        text_width = imgui.calc_text_size(value)[0]
                        centered_x = (imgui.get_window_width() - text_width) / 2
                        imgui.set_cursor_pos((centered_x, imgui.get_cursor_pos()[1]))
                        imgui.push_style_color(imgui.COLOR_TEXT, 1, 1, 0, 1)  
                        imgui.text(value)
                        imgui.pop_style_color()  # Reset to default color
                    elif label == "Description":
                        imgui.text_wrapped(f"{label}: {value}")  
                    elif label == "Coordinates":
                        imgui.text_wrapped(f"{label}: {value}")
                    else:
                        imgui.text(f"{label}: {value}")
                    
                    if i < len(attributes) - 1:
                        imgui.separator()

            imgui.end()

    def set_imgui_manager(self, imgui_manager):
        self.imgui_manager = imgui_manager
        self.interactions.imgui_manager = imgui_manager













