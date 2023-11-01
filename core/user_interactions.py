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
        self.total_pan_x,self.total_pan_y=[[]],[[]]
        self.dragx,self.dragy = 0,0
        self.diddrag=False
        self.i=0

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
                    self.total_pan_x.append([])
                    self.total_pan_y.append([])
                    self.i+=1
            case pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - self.last_mouse_x
                    dy = mouse_y - self.last_mouse_y
                    glTranslatef(dx * 3, -dy * 3, 0)
                    self.total_pan_x[self.i].append(self.last_mouse_x)
                    self.total_pan_y[self.i].append(self.last_mouse_y)
                    self.last_mouse_x, self.last_mouse_y = mouse_x, mouse_y
                    self.diddrag=True
            case pygame.VIDEORESIZE:
                width, height = event.size
                resize(width, height)
                self.imgui_manager.handle_resize(width, height)

    def selectionZoom(self,radius,pos):
        x,y,z=pos
        if self.diddrag:
            for i in range(len(self.total_pan_x)):
                if self.total_pan_x[i]!=[]:
                    self.dragx += (self.total_pan_x[i][0]-self.total_pan_x[i][len(self.total_pan_x[i])-1]) 
                    self.dragy += (self.total_pan_y[i][len(self.total_pan_y[i])-1]-self.total_pan_y[i][0])
            glTranslatef(self.dragx*3,self.dragy*3,0)
        if radius != 100:
            change_distance = abs(self.CAMERA_DISTANCE+500+z*1000)
        else:
            change_distance = abs(self.CAMERA_DISTANCE+500)
        self.CAMERA_DISTANCE = self.CAMERA_DISTANCE + change_distance
        glTranslatef(-x*1000-self.centerx,-y*1000-self.centery, change_distance)
        self.centerx,self.centery = -x*1000,-y*1000
        self.dragx,self.dragy = 0,0
        self.total_pan_x,self.total_pan_y=[[]],[[]]
        self.diddrag = False
        self.i=0