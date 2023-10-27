import pygame
import imgui
from OpenGL.GL import *
from core.imgui_manager import ImGuiManager
from imgui.integrations.pygame import PygameRenderer
from core.user_interactions import UserInteractions

#from core.user_interactions import UserInteractions
class CenterButton():
    def __init__(self):
        self.button_width = 150
        self.button_height = 50
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.camera_position = self.width/2, self.height/2
        self.initial_position = self.width/2, self.height/2
        
    def center(self):
        UserInteractions.CAMERA_DISTANCE = UserInteractions.INITIAL_CAMERA_DISTANCE
        glLoadIdentity()  # Reset the modelview matrix to identity
        glTranslatef(0, 0, UserInteractions.CAMERA_DISTANCE)

    def draw_button(self):
        # Define the size and position of the ImGui window for the button
        
        button_x = self.width - self.button_width
        button_y = self.height - self.button_height

        # Create the ImGui window for the button
        imgui.set_next_window_position(button_x, button_y)
        imgui.set_next_window_size(self.button_width, self.button_height)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        if imgui.button("Center"):
            self.center()

        imgui.end()

    def update_window_size(self, width, height):
        self.width = width
        self.height = height
        self.calculate_button_position(width, height)

    def calculate_button_position(self, width, height):
        button_x = width - self.button_width
        button_y = height - self.button_height
        imgui.set_next_window_position(button_x, button_y)
        imgui.set_next_window_size(self.button_width, self.button_height)

            