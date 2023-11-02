import pygame
import imgui
from imgui.integrations.pygame import PygameRenderer

class GuiManager:
    def __init__(self):
        self.renderer = self.setup_imgui()
        self.calender_widget = None

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
        self.render_infobox(solar_system)

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