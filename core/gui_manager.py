import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
import time
import datetime
from imgui.integrations.pygame import PygameRenderer

class GuiManager:
    def __init__(self):
        self.renderer = self.setup_imgui()
        self.error_message = ""
        self.error_display_time = 0
        self.show_date_input = False
        self.date_input = {'day': '', 'month': '', 'year': ''}
        self.show_labels = False
        self.show_celestial_body_selector = False

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
        """Start a new ImGui frame."""
        imgui.new_frame()

    def end_frame(self):
        """End the current ImGui frame and render it."""
        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def render_ui(self, solar_system, date_manager, user_interactions):
        self.render_date_selector(date_manager)
        self.render_infobox(solar_system)
        self.render_celestial_body_selector(solar_system)
        self.render_center_button(user_interactions)
        self.render_label_toggle_button()

    def process_event(self, event):
        """
        Process a single Pygame event and pass it to ImGui.
        """
        if self.renderer is not None:
            self.renderer.process_event(event)

    def render_celestial_body_selector(self, solar_system):
        """
        Renders a button and dropdown menu to select a celestial body, with bodies categorized by their 'category' attribute.
        :param solar_system: An instance of the SolarSystem class
        """
        imgui.set_next_window_position(65, 40)  # Adjust the position as needed
        imgui.begin("Celestial Body Selector", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        # Button to show/hide the dropdown menu
        if imgui.button("Pick Body"):
            self.show_celestial_body_selector = not self.show_celestial_body_selector

        # If the dropdown is to be shown
        if self.show_celestial_body_selector:
            # Sort celestial bodies into categories
            categories = {}
            for body in solar_system.space_bodies:
                category = body.category  # Access the category attribute of the celestial body
                if category not in categories:
                    categories[category] = []
                categories[category].append(body.name)

            # Get the currently selected body's name, or a default string if none is selected
            current_selection = solar_system.selected_planet.name if solar_system.selected_planet else "Select a Body"
            
            # Start the combo box
            if imgui.begin_combo("##celestial_body_combo", current_selection):
                for category, bodies in categories.items():
                    if imgui.tree_node(category):
                        for body_name in bodies:
                            # When a selectable item is clicked, update the selected planet in the solar_system
                            _, selected = imgui.selectable(body_name, current_selection == body_name)
                            if selected:
                                # Find and set the selected celestial body
                                for body in solar_system.space_bodies:
                                    if body.name == body_name:
                                        solar_system.selected_planet = body
                                        break
                                self.show_celestial_body_selector = False  # Optionally hide the selector after a selection
                                # Additional logic can be added here if needed
                        imgui.tree_pop()
                imgui.end_combo()

        imgui.end()

    def render_infobox(self, solar_system):
        if solar_system.is_infobox_visible() and solar_system.get_selected_planet() and solar_system.get_clicked_mouse_position():
            infobox_x, infobox_y, total_height = self.setup_infobox_position(solar_system)
            attributes = self.get_infobox_attributes(solar_system)
            
            imgui.set_next_window_position(infobox_x, infobox_y)
            imgui.set_next_window_size(300, total_height)
            
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
            imgui.begin("Info Box", solar_system.is_infobox_visible(), flags)
            
            self.render_infobox_content(attributes)
            
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
            description_width = 280
            total_height += imgui.calc_text_size(f"Description: {selected_planet.description}", wrap_width=description_width)[1] - text_height
        padding = 10
        total_height += 2 * padding
        
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

        screen_coords = gluProject(x*1500, y*1500, z*1500, modelview, projection, viewport)
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
        imgui.begin(f"Label {body.name}", flags=flags)

        # Render the celestial body's name inside the window
        imgui.text(body.name)

        # End the window
        imgui.end()

    def render_label_toggle_button(self):
        imgui.set_next_window_position(65, 0)
        self.set_date_selector_style()
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
        self.set_date_selector_style()
        self.begin_date_selector_window()
        self.render_input_date_toggle_button()
        self.render_separator()
        if self.show_date_input:
            self.render_date_input_fields(date_manager)
        self.end_date_selector_window()
        self.reset_style()

    def set_date_selector_window_position(self):
        imgui.set_next_window_position(175, 0) 

    def set_date_selector_style(self):
        style = imgui.get_style()
        style.window_border_size = 1.0
        style.window_rounding = 5.0
        style.frame_rounding = 5.0
        
    def begin_date_selector_window(self):
        window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE
        imgui.begin("Date Selector", flags=window_flags)

    def render_input_date_toggle_button(self):
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Input Date"):
            self.show_date_input = not self.show_date_input
        imgui.pop_style_color(1)

    def render_separator(self):
        imgui.push_style_color(imgui.COLOR_SEPARATOR, 1.0, 1.0, 1.0, 1.0)
        imgui.separator()
        imgui.pop_style_color()

    def render_date_input_fields(self, date_manager):
        imgui.text("Enter date (MM/DD/YYYY):")
        self.render_date_inputs()
        self.render_confirm_button(date_manager)
        self.render_reset_button(date_manager)
        self.display_error_message()

    def render_date_inputs(self):
        small_input_width = 23.5
        large_input_width = 37
        imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 1.0, 1.0, 1.0)
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0.2, 0.2, 0.2, 1.0)
        self.render_input_field("##month", self.date_input['month'], small_input_width, 2, "/")
        self.render_input_field("##day", self.date_input['day'], small_input_width, 2, "/")
        self.render_input_field("##year", self.date_input['year'], large_input_width, 4)
        imgui.pop_style_color(2)

    def render_input_field(self, label, value, width, buffer_size, separator=None):
        imgui.push_item_width(width)
        changed, self.date_input[label.strip('#')] = imgui.input_text(label, value, buffer_size)
        imgui.pop_item_width()
        if separator:
            imgui.same_line(spacing=10)
            imgui.text(separator)
            imgui.same_line(spacing=10)

    def render_confirm_button(self, date_manager):
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Confirm"):
            self.handle_date_confirmation(date_manager)
        imgui.pop_style_color(1)

    def render_reset_button(self, date_manager):
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Reset"):
            self.reset_to_current_date(date_manager)
        imgui.pop_style_color(1)

    def reset_to_current_date(self, date_manager):
        """Reset the date to the current date."""
        now = datetime.datetime.utcnow()
        date_manager.set_date(now.month, now.day, now.year)
        self.show_date_input = False
        self.error_message = "" 

    def display_error_message(self):
        if self.error_message:
            current_time = time.time()
            if current_time - self.error_display_time < 3:
                imgui.same_line()
                imgui.text_colored(self.error_message, 1.0, 0.0, 0.0)
            else:
                self.error_message = ""

    def end_date_selector_window(self):
        imgui.end()

    def reset_style(self):
        style = imgui.get_style()
        style.window_rounding = 0.0
        style.frame_rounding = 0.0
        
    def set_center_button_window_position(self):
        imgui.set_next_window_position(0, 0)
        
    def begin_center_button(self):
        imgui.set_next_window_size(63.5, 0)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        
    def render_center_button(self, user_interactions):
        self.set_date_selector_style()
        self.set_center_button_window_position()
        self.begin_center_button()
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Center"):
            print('Center button pressed')
            glLoadIdentity()
            user_interactions.center_camera()

        imgui.pop_style_color(1)

        self.render_separator()

        imgui.end()
        
        self.reset_style()

    def handle_date_confirmation(self, date_manager):
        try:
            # Check if any of the date fields are empty or placeholders
            if (self.date_input['day'] in ['', 'DD'] or
                self.date_input['month'] in ['', 'MM'] or
                self.date_input['year'] in ['', 'YYYY']):
                raise ValueError("Invalid date. Please enter a valid date.")

            # Convert the input strings to integers
            day = int(self.date_input['day'])
            month = int(self.date_input['month'])
            year = int(self.date_input['year'])

            # Check if the year is within the valid range
            if year > 2050:
                raise ValueError("Year must be before 2050.")
            if year < 2000:
                raise ValueError("Year must be after 1900.")

            # Validate the date using a helper method
            if not self.is_valid_date(year, month, day):
                raise ValueError("Invalid date. Please enter a valid date.")

            # If the date is valid, set it in the date manager
            date_manager.set_date(month, day, year)
            self.show_date_input = False 
            self.error_message = ""  
        except ValueError as e:
            # Display the error message
            self.error_message = str(e)
            self.error_display_time = time.time()  # Record the time when the error occurred

    def is_valid_date(self, year, month, day):
        """Check if the date is valid."""
        try:
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False

    def get_infobox_attributes(self, solar_system):
        selected_planet = solar_system.get_selected_planet()
        attributes = [
            ("Name", selected_planet.name),
            ("Description", selected_planet.description),
            ("Diameter", selected_planet.diameter),
            ("Mass", selected_planet.mass),
            ("Gravitational Acceleration", selected_planet.gravity),
            ("Average Temperature", selected_planet.avg_temperature),
            ("Distance to Earth", selected_planet.AU),
            ("Orbit Distance", selected_planet.orbit_distance),
            ("Day", selected_planet.day),
            ("Year", selected_planet.year)
        ]
        return attributes

    def render_infobox_content(self, attributes):
        padding = 10
        imgui.set_cursor_pos((imgui.get_cursor_pos()[0], imgui.get_cursor_pos()[1] + padding))
        for i, (label, value) in enumerate(attributes):
            if value: 
                if label == "Name":
                    text_width = imgui.calc_text_size(value)[0]
                    centered_x = (imgui.get_window_width() - text_width) / 2
                    imgui.set_cursor_pos((centered_x, imgui.get_cursor_pos()[1]))
                    imgui.push_style_color(imgui.COLOR_TEXT, 1, 1, 0, 1)  
                    imgui.text(value)
                    imgui.pop_style_color()
                elif label == "Description":
                    imgui.text_wrapped(f"{label}: {value}")  
                else:
                    imgui.text(f"{label}: {value}")
                if i < len(attributes) - 1:
                    imgui.separator()

    def handle_resize(self, width, height):
        """Update the display size for ImGui."""
        imgui.get_io().display_size = width, height




