import pygame
import imgui
from imgui.integrations.pygame import PygameRenderer
       
class ImGuiManager:
    def __init__(self):
        self.renderer = self.setup_imgui()

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
        