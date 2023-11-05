import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class UserInteractions:
    def __init__(self, window_manager, gui_manager):
        # Zooming and panning parameters
        self.gui_manager = gui_manager
        self.window_manager = window_manager
        self.screen = self.window_manager.screen
        self.skybox_eigth_size = 300000/10 # Same size as in solar_system.py
        self.LINEAR_ZOOM_AMOUNT = 450.0
        self.dragging = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        self.INITIAL_CAMERA_DISTANCE = -15000
        self.CAMERA_DISTANCE = self.INITIAL_CAMERA_DISTANCE
        self.MIN_ZOOM_IN = -500
        self.MAX_ZOOM_OUT = -10000
        self.centerx, self.centery = 0,0
        self.total_pan_x,self.total_pan_y=[[]],[[]]
        self.dragx,self.dragy = 0,0
        self.diddrag=False
        self.i=0

        self.MIN_ZOOM_IN = 400
        self.MAX_ZOOM_OUT = -50000

        # Camera position limits
        self.camera_limits = {
            'left': -self.skybox_eigth_size,
            'right': self.skybox_eigth_size,
            'up': self.skybox_eigth_size,
            'down': -self.skybox_eigth_size,
            'forward': self.MIN_ZOOM_IN,
            'backward': self.MAX_ZOOM_OUT
        }

        self.camera_position = [0, 0, self.CAMERA_DISTANCE]
        
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

                    # Calculate the new camera position
                    new_camera_x = self.camera_position[0] + dx * 15
                    new_camera_y = self.camera_position[1] - dy * 15

                    # Clamp the camera position to the defined limits
                    new_camera_x = max(min(new_camera_x, self.camera_limits['right']), self.camera_limits['left'])
                    new_camera_y = max(min(new_camera_y, self.camera_limits['up']), self.camera_limits['down'])

                    # Update the camera position
                    glTranslatef(new_camera_x - self.camera_position[0], new_camera_y - self.camera_position[1], 0)
                    self.camera_position[0] = new_camera_x
                    self.camera_position[1] = new_camera_y

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
                self.gui_manager.handle_resize(width, height)

    def get_camera_position(self):
        modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_position = [-modelview_matrix[3][i] for i in range(3)]
        return camera_position
    
    def get_camera_distance(self):
        return self.CAMERA_DISTANCE
    
    def center_camera(self):
        glLoadIdentity()
        glTranslatef(0, 0, self.CAMERA_DISTANCE)
        # Update the internal camera position state
        self.camera_position = [0, 0, self.CAMERA_DISTANCE]
