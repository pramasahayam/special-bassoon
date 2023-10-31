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
        self.centerx, self.centery = 0,0
        self.total_pan_x,self.total_pan_y=0,0
        self.dragx,self.dragy = 0,0
        self.diddrag=False

    def handle_event(self, event, resize):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1:
                        self.dragging = True
                        self.diddrag= True
                        self.last_mouse_x, self.last_mouse_y = event.pos
                        print("in1", self.last_mouse_x)
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
                    self.total_pan_x,self.total_pan_y=self.last_mouse_x, self.last_mouse_y
                    print("in2", self.last_mouse_x)
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
                self.imgui_manager.handle_resize(width, height)

    def selectionZoom(self,radius,pos,eventpos):
        x,y,z=pos
        ex,ey=eventpos
        # if self.diddrag:
        #     print("in")
        #     print(ex)
        #     print(self.total_pan_x)
        #     self.dragx = (-self.total_pan_x) 
        #     self.dragy = (-self.total_pan_y)
        #     #glTranslatef(self.dragx,self.dragy, 0)
        #     print(self.dragx)
        # if self.dragging:
        #     mouse_x, mouse_y = eventpos
        #     dx = mouse_x - self.last_mouse_x
        #     dy = mouse_y - self.last_mouse_y
        #     self.total_pan_x += dx
        #     self.total_pan_y += dy
        #     glTranslatef(dx * 3, -dy * 3, 0)
        #     self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
        change_distance = abs(self.CAMERA_DISTANCE+radius)-500
        self.CAMERA_DISTANCE = self.CAMERA_DISTANCE + change_distance
        #print(self.dragx)
        glTranslatef(-x*1000-self.centerx,-y*1000-self.centery, change_distance)
        #glTranslatef(-x*1000-self.centerx+self.dragx,-y*1000-self.centery+self.dragy, change_distance)
        self.centerx,self.centery = -x*1000,-y*1000
        #self.dragx,self.dragy = 0,0