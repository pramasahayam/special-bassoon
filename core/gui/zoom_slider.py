import imgui

class ZoomSlider:
    def __init__(self, set_common_style, window_manager):
        self.set_common_style = set_common_style
        self.window_manager = window_manager
        self.zoom = 58.3  # Initial zoom value

    def render(self, user_interactions):
        self.set_common_style()
        imgui.set_next_window_position(0, self.window_manager.HEIGHT - 60)
        imgui.begin("Zoom Slider", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        # Centering the word "Zoom" above the slider
        text_width = imgui.calc_text_size("Zoom")[0]
        window_width = imgui.get_window_width()
        imgui.set_cursor_pos(((window_width - text_width) / 2, imgui.get_cursor_pos()[1]))
        imgui.text("Zoom")

        # Adjust the item width to fit the slider neatly in the window
        imgui.push_item_width(window_width * 0.8)
        changed, new_zoom = imgui.slider_float(
            "##zoom",  # Using an ID to hide the label next to the slider
            self.zoom,
            min_value=0.0, max_value=100.0,
            format=""  # Removing the display of the zoom value
        )

        if changed:
            self.zoom = new_zoom
            # Smoothing the zoom transition
            new_camera_value = (60000 * (new_zoom / 100)) - 50000
            user_interactions.zoom_slider(new_camera_value)

        imgui.pop_item_width()
        imgui.end()
