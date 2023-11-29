import imgui

class TrajectoryMenu:
    def __init__(self, set_common_style, render_separator, trajectory_plotter):
        self.trajectory_plotter = trajectory_plotter
        self.show_trajectory_menu = False
        self.selected_celestial_bodies = [None, None]
        self.set_common_style = set_common_style
        self.render_separator = render_separator

    def render(self, solar_system):
        self.solar_system = solar_system
        self.set_common_style()

        imgui.set_next_window_position(518, 0)
        imgui.begin("Plot Trajectory", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE)

        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Plot Trajectory"):
            self.show_trajectory_menu = not self.show_trajectory_menu
        imgui.pop_style_color(1)

        self.render_separator()

        if self.show_trajectory_menu:
            self._render_body_selection()

        imgui.end()
    def _render_body_selection(self):
        dropdown_width = 150
        for i in range(2):
            label = f"Body {i+1}:"
            imgui.text(label)
            imgui.same_line()

            imgui.push_item_width(dropdown_width)
            current_selection = self.selected_celestial_bodies[i].name if self.selected_celestial_bodies[i] else "Select Object"
            if imgui.begin_combo(f"##body_selector_{i}", current_selection):
                self._populate_categories_and_handle_selection(i)
                imgui.end_combo()
            imgui.pop_item_width()

        if imgui.button("Confirm"):
            self._handle_confirmation()

    def _populate_categories_and_handle_selection(self, index):
        categories = self._categorize_celestial_bodies()
        for category, bodies in categories.items():
            if imgui.tree_node(category):
                for body_name in bodies:
                    _, selected = imgui.selectable(body_name, self.selected_celestial_bodies[index] and self.selected_celestial_bodies[index].name == body_name)
                    if selected:
                        self._handle_trajectory_body_selection(index, body_name)
                imgui.tree_pop()

    def _handle_trajectory_body_selection(self, index, body_name):
        for body in self.solar_system.space_bodies:
            if body.name == body_name:
                self.selected_celestial_bodies[index] = body
                break

    def _handle_confirmation(self):
        if self.selected_celestial_bodies[0] is not None and self.selected_celestial_bodies[1] is not None:
            # Retrieve indices of the selected celestial bodies
            origin_index = self.solar_system.space_bodies.index(self.selected_celestial_bodies[0])
            destination_index = self.solar_system.space_bodies.index(self.selected_celestial_bodies[1])

            # Calculate the trajectory
            trajectory_points, total_deltav, transfer_time = self.trajectory_plotter.calculate_trajectory(
                origin_index, destination_index
            )

            # Store these trajectory points for rendering
            self.trajectory_plotter.set_trajectory_points(trajectory_points)

            # Optionally display or log the total delta-v and transfer time
            print(f"Total Delta-V: {total_deltav}, Transfer Time: {transfer_time} days")
        else:
            print("Please select two celestial bodies.")

    def _categorize_celestial_bodies(self):
        categories = {}
        for body in self.solar_system.space_bodies:
            category = body.category
            if category not in categories:
                categories[category] = []
            categories[category].append(body.name)
        return categories
    
    def set_trajectory_plotter(self, trajectory_plotter):
        """
        Sets the trajectory plotter instance for the menu.
        """
        self.trajectory_plotter = trajectory_plotter
