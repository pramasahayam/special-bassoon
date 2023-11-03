import pygame
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
        self.date_input = {
            'day': 'DD',
            'month': 'MM',
            'year': 'YYYY'
        }

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

    def render_ui(self, solar_system, date_manager):
        self.render_date_selector(date_manager)
        self.render_infobox(solar_system)

    def process_event(self, event):
        """
        Process a single Pygame event and pass it to ImGui.
        """
        if self.renderer is not None:
            self.renderer.process_event(event)

    def render_infobox(self, solar_system):
        if solar_system.is_infobox_visible() and solar_system.get_selected_planet() and solar_system.get_clicked_mouse_position():
            infobox_x, infobox_y, total_height = self.setup_infobox_position(solar_system)
            attributes = self.get_infobox_attributes(solar_system)
            
            # Set the position and size of the ImGui window
            imgui.set_next_window_position(infobox_x, infobox_y)
            imgui.set_next_window_size(300, total_height)
            
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE
            imgui.begin("Info Box", solar_system.is_infobox_visible(), flags)
            
            self.render_infobox_content(attributes)
            
            imgui.end()

    def render_date_selector(self, date_manager):
        # Set the initial position for the date selector window
        imgui.set_next_window_position(50, 0)

        # Begin the date selector window with the appropriate flags
        window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE
        imgui.begin("Date Selector", flags=window_flags)

        # Button to toggle the visibility of the date input section
        if imgui.button("Input Date"):
            self.show_date_input = not self.show_date_input

        # If the button is pressed, show the input section
        if self.show_date_input:
            imgui.text("Enter date (MM/DD/YYYY):")
            imgui.push_item_width(50)
            changed_month, self.date_input['month'] = imgui.input_text("##month", self.date_input['month'], 3)
            imgui.same_line(spacing=10)
            imgui.text("/")
            imgui.same_line(spacing=10)
            changed_day, self.date_input['day'] = imgui.input_text("##day", self.date_input['day'], 3)
            imgui.same_line(spacing=10)
            imgui.text("/")
            imgui.same_line(spacing=10)
            changed_year, self.date_input['year'] = imgui.input_text("##year", self.date_input['year'], 5)
            imgui.pop_item_width()

            # Confirm Date button
            if imgui.button("Confirm Date"):
                try:
                    day = int(self.date_input['day'])
                    month = int(self.date_input['month'])
                    year = int(self.date_input['year'])

                    # Check if the year is within the valid range
                    if year > 2050:
                        raise ValueError("Year must be 2050 or earlier.")

                    # Validate the date
                    if not self.is_valid_date(year, month, day):
                        raise ValueError("Invalid date. Please enter a valid date.")

                    # If the date is valid, set it in the date manager
                    date_manager.set_date(month, day, year)
                    self.show_date_input = False  # Optionally hide the input fields after confirmation
                    self.error_message = ""  # Clear any previous error message
                except ValueError as e:
                    # Display the error message
                    self.error_message = str(e)
                    self.error_display_time = time.time()  # Record the time when the error occurred

            # Display error message if present
            if self.error_message:
                current_time = time.time()
                # Check if less than 1 second has passed since the error was recorded
                if current_time - self.error_display_time < 3:
                    imgui.same_line()
                    imgui.text_colored(self.error_message, 1.0, 0.0, 0.0)  # Red text
                else:
                    self.error_message = ""  # Clear the error message after 1 second

        # End the date selector window
        imgui.end()

    def is_valid_date(self, year, month, day):
        """Check if the date is valid."""
        try:
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False

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