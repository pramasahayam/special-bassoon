import pygame
import imgui
from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import *
       
class GuiManager:
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
        
    def process_event(self, event):
        """
        Process a single Pygame event and pass it to ImGui.
        """
        if self.renderer is not None:
            self.renderer.process_event(event)

    def handle_resize(self, width, height):
        """Update the display size for ImGui."""
        imgui.get_io().display_size = width, height
        
    def render_ui(self):
        self.render_center_button()
    
    def set_date_selector_style(self):
        style = imgui.get_style()
        style.window_rounding = 5.0
        style.frame_rounding = 5.0
    
    def reset_date_selector_style(self):
        style = imgui.get_style()
        style.window_rounding = 0.0
        style.frame_rounding = 0.0
        
    def set_center_button_window_position(self):
        imgui.set_next_window_position(0, 0)
        
    def begin_center_button(self):
        imgui.set_next_window_size(65, 40)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        
    def render_center_button(self):
        self.set_date_selector_style()
        self.set_center_button_window_position()
        self.begin_center_button()
        
        if imgui.button("Center"):
            print('Center button pressed')
            glLoadIdentity()
            glTranslatef(0, 0, -5000) 

        imgui.end()
        
        self.reset_date_selector_style()
        