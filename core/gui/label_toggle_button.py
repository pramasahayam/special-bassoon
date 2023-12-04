import imgui
from OpenGL.GL import glGetDoublev, glGetIntegerv, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX, GL_VIEWPORT
from OpenGL.GLU import gluProject

class LabelToggleButton:
    def __init__(self, set_common_style):
        self.set_common_style = set_common_style
        self.show_labels = False

    def render(self, solar_system, date_manager):
        self._render_toggle_button()
        if self.show_labels:
            for body in solar_system.space_bodies:
                if not body.orbital_center:
                    self._render_body_label(body, date_manager.get_current_date())

    def _render_toggle_button(self):
        imgui.set_next_window_position(71, 0)
        self.set_common_style()
        imgui.begin("Label Toggle", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        
        if imgui.button("Toggle Labels"):
            self.show_labels = not self.show_labels

        imgui.pop_style_color(1)
        imgui.end()

    def _render_body_label(self, body, current_time):
        label_x, label_y = self._calculate_label_position(body, current_time)
        if label_x is not None and label_y is not None:
            self.set_common_style()
            imgui.set_next_window_position(label_x, label_y)
            flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR
            imgui.begin(f"Label {body.name}", flags=flags)
            imgui.text(body.name)
            imgui.end()

    def _calculate_label_position(self, body, t):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        x, y, z = body.compute_position(t)
        screen_coords = gluProject(x, y, z, modelview, projection, viewport)
        if screen_coords is None:
            return None, None
        screen_x, screen_y, _ = screen_coords
        return (screen_x, viewport[3] - screen_y)
