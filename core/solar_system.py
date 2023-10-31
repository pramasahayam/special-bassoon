import pygame
import imgui
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from core.user_interactions import UserInteractions
from core.window_management import WindowManager
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon#, Europa, Ganymede, Titan, Deimos, Phobos, Callisto, Io, Iapetus, Oberon, Titania, Umbriel, Ariel

class SolarSystem:
    def __init__(self, imgui_manager=None):
        self.imgui_manager = imgui_manager
        self.window = WindowManager()
        self.interactions = UserInteractions(self.window, self.imgui_manager)
        self.clicked_mouse_position = None
        
        # List of space bodies in our solar system
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto(), Moon(Earth())#, Europa(Jupiter()), Titan(Saturn()), Deimos(Mars()),
            # Phobos(Mars()), Callisto(Jupiter()), Io(Jupiter()), Iapetus(Saturn()), Oberon(Uranus()), Titania(Uranus()), Umbriel(Uranus()), Ariel(Uranus()), 
            # Ganymede(Jupiter())
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

                        # First, check for intersections with celestial bodies
                        for body in self.space_bodies:
                            body_position = np.array(body.compute_position(t))
                            scaled_body_position = body_position * 1000
                            if self.intersects_sphere(ray_origin, ray_direction, scaled_body_position, body.radius) == "body":
                                self.selected_planet = body
                                self.infobox_visible = True
                                self.clicked_mouse_position = event.pos
                                print(f"Clicked on: {self.selected_planet.name}")
                                return  # Exit the function as soon as we find an intersection with a celestial body

                        # If no celestial body is intersected, then check for intersections with the rings
                        for body in self.space_bodies:
                            body_position = np.array(body.compute_position(t))
                            scaled_body_position = body_position * 1000
                            if self.intersects_sphere(ray_origin, ray_direction, scaled_body_position, body.radius) == "ring":
                                print(f"Ring of {body.name} was clicked!")
                                # Here, you can add the logic to zoom the camera into the celestial body
                                break

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

        # Quadratic formula components for the celestial body
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - sphere_radius * sphere_radius

        # Discriminant for the celestial body
        discriminant = b * b - 4 * a * c

        if discriminant > 0:
            return "body"

        # Check for intersection with the ring
        if sphere_radius <= 3:
            ring_radius = sphere_radius * 200
        elif sphere_radius <= 11:
            ring_radius = sphere_radius * 30
        elif sphere_radius >= 3:
            ring_radius = sphere_radius * 8

        oc_ring = ray_origin - sphere_center
        a_ring = np.dot(ray_direction, ray_direction)
        b_ring = 2.0 * np.dot(oc_ring, ray_direction)
        c_ring = np.dot(oc_ring, oc_ring) - ring_radius * ring_radius

        # Discriminant for the ring
        discriminant_ring = b_ring * b_ring - 4 * a_ring * c_ring

        if discriminant_ring > 0:
            return "ring"

        return None

    def draw_body(self, body, t):
        glPushMatrix()  # Save the current OpenGL state

        # Compute the position of the celestial body
        x, y, z = body.compute_position(t)
        glTranslatef(x * 1000, y * 1000, z * 1000)  # Scaling factor for visualization

        # Draw the ring around the celestial body if it's not selected
        if body != self.selected_planet and not body.orbital_center:
            glDisable(GL_TEXTURE_2D)  # Ensure textures are disabled for the ring
            self.draw_ring(body.radius)

        # Now, apply the rotation for the celestial body
        glRotatef(30, 0, 1, 0)  # Rotate for visualization

        # Existing code to draw the celestial body
        quad = gluNewQuadric()

        # If the body has a texture, bind it
        if body.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, body.texture_id)
            gluQuadricTexture(quad, GL_TRUE)
        else:
            glDisable(GL_TEXTURE_2D)

        gluSphere(quad, body.radius*2, 100, 100)

        glPopMatrix()  # Restore the saved OpenGL state

    def draw_ring(self, body_radius):
        if body_radius <= 3:
            ring_radius = body_radius * 200
        elif body_radius <= 11:
            ring_radius = body_radius * 30
        elif body_radius >= 3:
            ring_radius = body_radius * 7
        num_segments = 100  # Adjust for smoother circle

        glBegin(GL_LINE_LOOP)
        for i in range(num_segments):
            theta = 2.0 * np.pi * float(i) / float(num_segments)
            dx = ring_radius * np.cos(theta)
            dy = ring_radius * np.sin(theta)
            glVertex2f(dx, dy)
        glEnd()
        
    def get_selected_planet(self):
        return self.selected_planet

    def is_infobox_visible(self):
        return self.infobox_visible

    def get_clicked_mouse_position(self):
        return self.clicked_mouse_position

    def set_imgui_manager(self, imgui_manager):
        self.imgui_manager = imgui_manager
        self.interactions.imgui_manager = imgui_manager
