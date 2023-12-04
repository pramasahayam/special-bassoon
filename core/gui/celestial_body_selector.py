import imgui

class CelestialBodySelector:
    def __init__(self, set_common_style, render_separator):
        self.set_common_style = set_common_style
        self.render_separator = render_separator

    def render(self, solar_system, user_interactions, date_manager):
        imgui.set_next_window_position(388, 0)
        self.set_common_style()
        imgui.begin("Celestial Body Selector", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)

        current_selection_label = solar_system.selected_planet.name if solar_system.selected_planet else "Select Object"
        desired_width = 125
        imgui.push_item_width(desired_width)

        if imgui.begin_combo("##celestial_body_combo", current_selection_label):
            categories = self.categorize_celestial_bodies(solar_system)
            for category, bodies in categories.items():
                if imgui.tree_node(category):
                    for body_name in bodies:
                        _, selected = imgui.selectable(body_name, solar_system.selected_planet and solar_system.selected_planet.name == body_name)
                        if selected:
                            self.handle_body_selection(solar_system, body_name, user_interactions, date_manager)
                    imgui.tree_pop()
            imgui.end_combo()
        
        imgui.pop_item_width()
        imgui.pop_style_color(1)
        imgui.end()

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
