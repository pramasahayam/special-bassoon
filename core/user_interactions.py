import pygame
from pygame.locals import *
from OpenGL.GL import *

class UserInteractions:
    def __init__(self, screen):
        # Zooming and panning parameters
        self.screen = screen
        self.LINEAR_ZOOM_AMOUNT = 100.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -5000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE
        self.MIN_ZOOM_IN = -500
        self.MAX_ZOOM_OUT = -10000

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
                    glTranslatef(dx * 0.5, -dy * 0.5, 0)
                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)

    def show_info_box(self, body):
        print("Attempting to show info box for:", body.name)
        # Dimensions for the info box
        width, height = 300, 200
        x, y = 50, 50  # top-left position of the box

        # Create a semi-transparent surface for the info box
        info_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        info_surface.fill((50, 50, 50, 180))  # RGBA

        font = pygame.font.SysFont('Arial', 18)
        
        name_text = font.render(str(body.name), True, (255, 255, 255))
        description_text = font.render(str(body.description), True, (255, 255, 255))
        radius_text = font.render(f"Radius: {body.radius}", True, (255, 255, 255))
        orbital_text = font.render(f"Orbital Period: {body.orbital_period}", True, (255, 255, 255))

        info_surface.blit(name_text, (10, 10))
        info_surface.blit(description_text, (10, 40))
        info_surface.blit(radius_text, (10, 70))
        info_surface.blit(orbital_text, (10, 100))

        self.screen.blit(info_surface, (x, y))
        pygame.display.flip()
