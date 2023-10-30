import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class UserInteractions:
    def __init__(self, window_manager, imgui_manager):
        # Zooming and panning parameters
        self.imgui_manager = imgui_manager
        self.window_manager = window_manager
        self.screen = self.window_manager.screen
        self.LINEAR_ZOOM_AMOUNT = 400.0
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
                    glTranslatef(dx * 3, -dy * 3, 0)
                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
                self.imgui_manager.handle_resize(width, height)

    def selectionZoom(self,planet,radius,pos, eventpos):
        x,y,z=pos
        ex,ey=eventpos
        print(ex)
        print(ey)
        change_distance = abs(self.CAMERA_DISTANCE+radius)-500
        self.CAMERA_DISTANCE = self.CAMERA_DISTANCE + change_distance
        #rect=self.screen.get_rect(center=(0,0))
        #pygame.Rect.move_ip(rect, self.window_manager.WIDTH-x, self.window_manager.HEIGHT-y)
        #self.window_manager.screen.blit(self.window_manager.screen, rect)
        #center = screen.get_rect().center
        #screen.blit(planet, center)
        #screen.get_rect(center=(x,y,0))
        glTranslatef(ex-350,ey-150, change_distance)
