import pygame
import imgui
from OpenGL.GL import *

class CenterButton:
    def __init__(self):
        self.button_width = 65
        self.button_height = 40
        self.button_position = (0, 0)

    def update_window_size(self, width, height):
        self.calculate_button_position(width, height)
        
    def mouse_on_button(self, mouse_pos):
        button_x, button_y = self.button_position
        button_width, button_height = self.button_width, self.button_height

        mouse_x, mouse_y = mouse_pos

        return (
            button_x <= mouse_x <= button_x + button_width and
            button_y <= mouse_y <= button_y + button_height
        )
        
    def handle_click(self):
        glLoadIdentity()
        glTranslatef(0, 0, -5000) 

    def calculate_button_position(self, width, height):
        button_x = 0
        button_y = height - self.button_height
        self.button_position = (button_x, button_y)

    def draw_button(self):
        imgui.set_next_window_position(*self.button_position)
        imgui.set_next_window_size(self.button_width, self.button_height)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        if imgui.button("Center"):
            glLoadIdentity()
            glTranslatef(0, 0, -5000) 

        imgui.end()
