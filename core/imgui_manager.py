import pygame
import imgui
from imgui.integrations.pygame import PygameRenderer
from core.buttons import CenterButton
from OpenGL.GL import *
       
class ImGuiManager:
    def __init__(self):
        self.renderer = self.setup_imgui()
        self.center_button = CenterButton

    def setup_imgui(self):
        # Initialize ImGui
        imgui.create_context()
        imgui.get_io().display_size = pygame.display.Info().current_w, pygame.display.Info().current_h
        
        # Load the font
        io = imgui.get_io()
        font_path = "utils/fonts/TimesNewRoman.ttf"
        io.fonts.add_font_from_file_ttf(font_path, 16)  # 16 is the font size

        # Initialize the Pygame renderer for ImGui
        renderer = PygameRenderer()

        return renderer

    def start_frame(self, screen):
        """Start a new ImGui frame and handle Pygame events."""
        imgui.new_frame()
        for event in pygame.event.get():
            self.renderer.process_event(event)

    def end_frame(self):
        """End the current ImGui frame and render it."""
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def cleanup(self):
        """Cleanup resources when the application exits."""
        imgui.end_frame()
        imgui.shutdown()

    def handle_resize(self, width, height):
        """Update the display size for ImGui."""
        imgui.get_io().display_size = width, height
        
    def render_center_button(self, center_button):
        imgui.set_next_window_position(*center_button.button_position)  # Use the stored button position
        imgui.set_next_window_size(center_button.button_width, center_button.button_height) #
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        if imgui.button("Center"):
            """glLoadIdentity()  # Reset the modelview matrix to identity
            glTranslatef(0, 0, -5000)"""
            print("Button clicked!")  # Add a debug message

        imgui.end()
        