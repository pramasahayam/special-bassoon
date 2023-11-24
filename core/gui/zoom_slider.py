import imgui

class ZoomSlider:
    def __init__(self, set_common_style, window_height):
        self.set_common_style = set_common_style
        self.window_height = window_height
        self.zoom = 58.3  # Initial zoom value

    def render(self, user_interactions):
        self.set_common_style()
        imgui.set_next_window_position(0, self.window_height - 60)
        imgui.begin("Zoom Slider", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        imgui.push_item_width(imgui.get_window_width() * 0.5)
        changed, new_zoom = imgui.slider_float(
            "Zoom Slider", self.zoom,
            min_value=0.0, max_value=100.0,
            format="%.0f"
        )

        if changed:
            self.zoom = new_zoom
            new_camera_value = (60000 * (new_zoom / 100)) - 50000
            user_interactions.zoom_slider(new_camera_value)

        imgui.pop_item_width()
        imgui.text("Value: %s" % (self.zoom))
        imgui.end()
