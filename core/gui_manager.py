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
        self.zoom_slider = ZoomSlider(self.set_common_style, self.window_manager)
        self.renderer = self.setup_imgui()
        self.is_hovering_imgui = False
        self.is_using_imgui = False

    def setup_imgui(self):
        imgui.create_context()
        imgui.get_io().display_size = pygame.display.Info().current_w, pygame.display.Info().current_h

        io = imgui.get_io()
        font_path = "utils/fonts/OrbitronRegular400.ttf"
        io.fonts.add_font_from_file_ttf(font_path, 12)  # 16 is the font size

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

    def render_celestial_body_selector(self, solar_system, user_interactions, date_manager):
        # Initialize Window
        imgui.set_next_window_position(366, 0)
        self.set_common_style()
        imgui.begin("Celestial Body Selector", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)

        # Prepare ComboBox
        current_selection_label = solar_system.selected_planet.name if solar_system.selected_planet else "Select Object"
        desired_width = 125
        imgui.push_item_width(desired_width)

        # Populate Categories and Handle Selection
        if imgui.begin_combo("##celestial_body_combo", current_selection_label):
            self.populate_categories_and_handle_selection(solar_system, user_interactions, date_manager)
            imgui.end_combo()
        
        # Reset item width after the combo box
        imgui.pop_item_width()
        imgui.pop_style_color(1)
        self.render_separator()
        imgui.end()

    def populate_categories_and_handle_selection(self, solar_system, user_interactions, date_manager):
        categories = self.categorize_celestial_bodies(solar_system)
        for category, bodies in categories.items():
            if imgui.tree_node(category):
                for body_name in bodies:
                    _, selected = imgui.selectable(body_name, solar_system.selected_planet and solar_system.selected_planet.name == body_name)
                    if selected:
                        self.handle_body_selection(solar_system, body_name, user_interactions, date_manager)
                imgui.tree_pop()

    def categorize_celestial_bodies(self, solar_system):
        categories = {}
        for body in solar_system.space_bodies:
            category = body.category
            if category not in categories:
                categories[category] = []
            categories[category].append(body.name)
        return categories

    def handle_body_selection(self, solar_system, body_name, user_interactions, date_manager):
        for body in solar_system.space_bodies:
            if body.name == body_name:
                body_position = body.compute_position(date_manager.get_current_date())
                body_radius = body.radius
                user_interactions.focus_on_body(solar_system, body_position, body_radius)
                solar_system.selected_planet = None
                break

    def render_infobox(self, solar_system):
        if solar_system.is_infobox_visible() and solar_system.get_selected_planet() and solar_system.get_clicked_mouse_position():
            infobox_x, infobox_y, total_height = self.setup_infobox_position(solar_system)
            attributes = self.get_infobox_attributes(solar_system)

            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.1137, 0.1843, 0.2863, 0.2)
            imgui.set_next_window_position(infobox_x, infobox_y)
            imgui.set_next_window_size(300, total_height)
            
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
            self.set_common_style()
            imgui.begin("Info Box", solar_system.is_infobox_visible(), flags)
            
            self.render_infobox_content(attributes,solar_system.get_selected_planet().color)
            
            imgui.pop_style_color()
            imgui.end()

    def setup_infobox_position(self, solar_system):
        mouse_x, mouse_y = solar_system.get_clicked_mouse_position()
        offset_x = -350 
        offset_y = -150   
        infobox_x = mouse_x + offset_x
        infobox_y = mouse_y + offset_y
        
        text_height = imgui.get_text_line_height()
        separator_height = imgui.get_frame_height_with_spacing()
        
        selected_planet = solar_system.get_selected_planet()
        attributes = self.get_infobox_attributes(solar_system)
        
        total_height = sum(text_height for _, value in attributes if value)
        total_height += separator_height * (len([value for _, value in attributes if value]) - 1)
        if selected_planet.description:
            description_width = 500
            total_height += imgui.calc_text_size(f"Description: {selected_planet.description}", wrap_width=description_width)[1] #- text_height
        
        return infobox_x, infobox_y, total_height
  
    def render_labels(self, body, t):
        if self.show_labels:
            label_x, label_y = self.calculate_label_position(body, t)
            if label_x is not None and label_y is not None:
                self.render_label_for_body(body, label_x, label_y)

    def calculate_label_position(self, body, t):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        x, y, z = body.compute_position(t)

        screen_coords = gluProject(x, y, z, modelview, projection, viewport)
        if screen_coords is None:
            return None, None

        screen_x, screen_y, _ = screen_coords
        return (screen_x, viewport[3] - screen_y)  # Adjust for OpenGL's y-coordinate starting from the bottom.

    def render_label_for_body(self, body, label_x, label_y):
        # Set the next window position here
        imgui.set_next_window_position(label_x, label_y)

        # Set the window to be always on top, no title bar, no resize, etc.
        flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR

        # Begin the window and give it a unique name based on the celestial body's name
        self.set_common_style()
        imgui.begin(f"Label {body.name}", flags=flags)

        # Render the celestial body's name inside the window
        imgui.text(body.name)

        # End the window
        imgui.end()

    def render_label_toggle_button(self):
        imgui.set_next_window_position(65, 0)
        self.set_common_style()
        imgui.begin("Label Toggle", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Toggle Labels"):
            self.show_labels = not self.show_labels

        imgui.pop_style_color(1)

        self.render_separator()

        imgui.end()
        self.reset_style()

    def render_date_selector(self, date_manager):
        self.set_date_selector_window_position()
        self.set_common_style()
        self.begin_date_selector_window()
        self.render_input_date_toggle_button()
        self.render_separator()
        if self.show_date_input:
            self.render_date_input_fields(date_manager)
        self.end_date_selector_window()
        self.reset_style()

    def set_date_selector_window_position(self):
        imgui.set_next_window_position(175, 0) 

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
