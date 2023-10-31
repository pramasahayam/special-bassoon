import pygame
import imgui
from OpenGL.GL import *
from core.imgui_manager import ImGuiManager
from imgui.integrations.pygame import PygameRenderer
from core.user_interactions import UserInteractions

#from core.user_interactions import UserInteractions
class CenterButton():
    def __init__(self):
        self.button_width = 65
        self.button_height = 40
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.button_position = (0,0)

    def update_window_size(self, width, height):
        self.width = width
        self.height = height
        self.calculate_button_position(self.width, self.height)
        
    def calculate_button_position(self, width, height):
        button_x = 0 # Set the left edge of the button at the left edge of the window
        button_y = height - self.button_height  # Align the bottom of the button with the bottom of the window
        self.button_position = (button_x, button_y)  # Store the button position for drawing
        

    def draw_button(self):
        imgui.set_next_window_position(*self.button_position)  # Use the stored button position
        imgui.set_next_window_size(self.button_width, self.button_height)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        button_clicked = imgui.button("Center")

        if button_clicked:
            print("Button clicked!")  # Add a debug message

        imgui.end()
        return button_clicked
    
 