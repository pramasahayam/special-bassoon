import pygame
from OpenGL.GL import *

class UserInteractions:
    def __init__(self):
        # Zooming and panning parameters
        self.LINEAR_ZOOM_AMOUNT = 100.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -5000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE
        self.MIN_ZOOM_IN = -500
        self.MAX_ZOOM_OUT = -10000
        self.info_boxes = {}
        self.displayed_info_box = None

    def handle_event(self, event, resize, space_bodies, screen):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event, space_bodies, screen)
            case pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)
            case pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)

    def _handle_mouse_button_down(self, event, space_bodies, screen):
        match event.button:
            case 1:
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
                if self.displayed_info_box and not self.info_boxes[self.displayed_info_box].collidepoint(event.pos):
                    self.hide_info_box()
                else:
                    # Placeholder for planet picking
                    clicked_planet = None
                    if clicked_planet:
                        self.show_info_box(clicked_planet, screen)
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

    def _handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False

    def _handle_mouse_motion(self, event):
        if self.dragging:
            mouse_x, mouse_y = event.pos
            dx = mouse_x - self.last_mouse_x
            dy = mouse_y - self.last_mouse_y
            glTranslatef(dx * 0.5, -dy * 0.5, 0)
            self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y

    def show_info_box(self, planet, screen):
        # If there's already an info box displayed, hide it
        if self.displayed_info_box:
            self.hide_info_box()
        
        # Define the size and position of the info box
        box_width, box_height = 200, 100
        x, y = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, box_width, box_height)
        
        # Store this rectangle in the info_boxes dictionary
        self.info_boxes[planet.name] = rect
        self.displayed_info_box = planet.name
        
        # Draw the box using Pygame
        pygame.draw.rect(screen, (255, 255, 255), rect)
        
        # Use Pygame's font system to render text
        font = pygame.font.SysFont(None, 25)
        label = font.render(planet.name, True, (0, 0, 0))
        screen.blit(label, (x + 10, y + 10))
        label = font.render(planet.description, True, (0, 0, 0))
        screen.blit(label, (x + 10, y + 40))

    def hide_info_box(self):
        # Remove the info box rectangle from the dictionary
        if self.displayed_info_box:
            del self.info_boxes[self.displayed_info_box]
            self.displayed_info_box = None
