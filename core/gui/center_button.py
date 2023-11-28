import imgui

class CenterButton:
    def __init__(self, set_common_style, render_separator):
        self.set_common_style = set_common_style
        self.render_separator = render_separator

    def render(self, user_interactions):
        self.set_common_style()
        imgui.set_next_window_position(0, 0)
        imgui.begin("Center Button", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Center"):
            user_interactions.center_camera()

        imgui.pop_style_color(1)
        self.render_separator()
        imgui.end()
