import pygame
import imgui
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from core.user_interactions import UserInteractions
from core.window_management import WindowManager
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Europa, Ganymede, Titan, Deimos, Phobos, Callisto, Io, Iapetus, Oberon, Titania, Umbriel, Ariel

class SolarSystem:
    def __init__(self, imgui_manager=None):
        self.imgui_manager = imgui_manager
        self.window = WindowManager()
        self.interactions = UserInteractions(self.window, self.imgui_manager)
        self.clicked_mouse_position = None
        
        # List of space bodies in our solar system
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto(), Moon(Earth()), Europa(Jupiter()), Titan(Saturn()), Deimos(Mars()),
            Phobos(Mars()), Callisto(Jupiter()), Io(Jupiter()), Iapetus(Saturn()), Oberon(Uranus()), Titania(Uranus()), Umbriel(Uranus()), Ariel(Uranus()), 
            Ganymede(Jupiter())
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
                        ray_origin = np.array(self.interactions.get_camera_position())
                        ray_direction = self.compute_ray_from_mouse(event.pos)

                        for body in self.space_bodies:
                            body_position = np.array(body.compute_position(t))

                            distance_to_body = np.linalg.norm(body_position - ray_origin)

                            scaled_body_position = body_position * 1000
                            if self.intersects_sphere(ray_origin, ray_direction, scaled_body_position, body.visual_radius):

                                self.selected_planet = body
                                self.infobox_visible = True
                                self.clicked_mouse_position = event.pos
                                print(f"Clicked on: {self.selected_planet.name}")
                                break  # Exit the loop as soon as we find an intersection


    def compute_ray_from_mouse(self, mouse_pos):
        x, y = mouse_pos
        _, current_height = self.window.get_current_dimensions()

        # Convert mouse position to normalized device coordinates
        ndc_x = (2.0 * x) / self.window.WIDTH - 1.0
        ndc_y = 1.0 - (2.0 * y) / current_height

        # Convert NDC to clip space
        clip_coords = [ndc_x, ndc_y, -1.0, 1.0]  # -1.0 for forward direction, 1.0 for homogeneous coordinate

        # Multiply clip coordinates by the inverse projection matrix to get eye coordinates
        inv_projection = np.linalg.inv(glGetDoublev(GL_PROJECTION_MATRIX))
        eye_coords = np.dot(inv_projection, clip_coords)
        eye_coords = [eye_coords[0], eye_coords[1], -1.0, 0.0]  # Set forward direction

        # Multiply eye coordinates by the inverse view matrix to get world coordinates
        inv_view = np.linalg.inv(glGetDoublev(GL_MODELVIEW_MATRIX))
        world_coords = np.dot(inv_view, eye_coords)

        # The ray's direction in world space
        ray_direction = [world_coords[0], world_coords[1], world_coords[2]]
        ray_direction = ray_direction / np.linalg.norm(ray_direction)  # Normalize

        return ray_direction
    
    def intersects_sphere(self, ray_origin, ray_direction, sphere_center, sphere_radius):
        # Compute the vector from the ray's origin to the sphere's center
        oc = ray_origin - sphere_center

        # Quadratic formula components
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - sphere_radius * sphere_radius

        # Discriminant
        discriminant = b * b - 4 * a * c
        return discriminant > 0


    def draw_body(self, body, t):
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

        glRotatef(30, 0, 1, 0) # Rotate for visualization

        gluSphere(quad, body.visual_radius, 100, 100)
        glPopMatrix()

    def render_ui(self):
        t = self.space_bodies[0].ts.now()

        if self.infobox_visible and self.selected_planet and self.clicked_mouse_position:
            mouse_x, mouse_y = self.clicked_mouse_position
            
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
                ("Year",self.selected_planet.year)
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













