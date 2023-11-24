import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
import time
import datetime
from imgui.integrations.pygame import PygameRenderer
from core.gui.loading_screen import LoadingScreen
from core.gui.trajectory_menu import TrajectoryMenu
from core.gui.celestial_body_selector import CelestialBodySelector
from core.gui.date_selector import DateSelector
from core.gui.infobox import Infobox
from core.gui.label_toggle_button import LabelToggleButton
from core.gui.center_button import CenterButton
from core.gui.zoom_slider import ZoomSlider

class GuiManager:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.loading_screen = LoadingScreen(window_manager, self)
        self.trajectory_menu = TrajectoryMenu(self.set_common_style, self.render_separator)
        self.celestial_body_selector = CelestialBodySelector(self.set_common_style, self.render_separator)
        self.date_selector = DateSelector(self.set_common_style, self.render_separator)
        self.infobox = Infobox(self.set_common_style)
        self.label_toggle_button = LabelToggleButton(self.set_common_style, self.render_separator)
        self.center_button = CenterButton(self.set_common_style, self.render_separator)
        self.zoom_slider = ZoomSlider(self.set_common_style, self.window_manager.HEIGHT)
        self.renderer = self.setup_imgui()
        self.is_hovering_imgui = False
        self.is_using_imgui = False

    def setup_imgui(self):
        imgui.create_context()
        imgui.get_io().display_size = pygame.display.Info().current_w, pygame.display.Info().current_h

        io = imgui.get_io()
        font_path = "utils/fonts/TimesNewRoman.ttf"
        io.fonts.add_font_from_file_ttf(font_path, 16)  # 16 is the font size

        # Initialize the Pygame renderer for ImGui
        renderer = PygameRenderer()

        return renderer
            
    def start_frame(self):
        """
        Start a new ImGui frame and update interaction flags.
        """
        imgui.new_frame()

        # Reset flags at the start of each frame
        self.is_hovering_imgui = False
        self.is_using_imgui = False

    def end_frame(self):
        """End the current ImGui frame and render it."""
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def render_ui(self, solar_system, date_manager, user_interactions):
        self.date_selector.render(date_manager)
        self.infobox.render(solar_system)
        self.celestial_body_selector.render(solar_system, user_interactions, date_manager)
        self.center_button.render(user_interactions)
        self.trajectory_menu.render(solar_system)
        self.label_toggle_button.render(solar_system, date_manager)
        self.zoom_slider.render(user_interactions)

    def process_event(self, event):
        """
        Process a single Pygame event and pass it to ImGui.
        Also update ImGui interaction flags based on the event.
        """
        if self.renderer is not None:
            self.renderer.process_event(event)

            # Update flags based on ImGui state after processing the event
            io = imgui.get_io()
            self.is_hovering_imgui = io.want_capture_mouse
            self.is_using_imgui = io.want_capture_keyboard

    def is_imgui_hovered(self):
        """
        Check if ImGui is currently being hovered by the mouse.
        """
        return self.is_hovering_imgui
    
    def is_imgui_used(self):
        """
        Check if ImGui is currently capturing keyboard or mouse input.
        """
        return self.is_using_imgui

    def render_loading_screen(self, progress):
        """Delegate rendering of the loading screen to the LoadingScreen instance."""
        self.loading_screen.render(progress)

    def set_common_style(self):
        style = imgui.get_style()
        style.window_border_size = 1.0
        style.window_rounding = 5.0
        style.frame_rounding = 5.0
        
    def reset_style(self):
        style = imgui.get_style()
        style.window_rounding = 0.0
        style.frame_rounding = 0.0

    def render_separator(self):
        imgui.push_style_color(imgui.COLOR_SEPARATOR, 1.0, 1.0, 1.0, 1.0)
        imgui.separator()
        imgui.pop_style_color()

    def handle_resize(self, width, height):
        # Update ImGui's display size
        imgui.get_io().display_size = width, height
    
