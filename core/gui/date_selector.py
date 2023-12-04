import imgui
import datetime
import time

class DateSelector:
    def __init__(self, set_common_style, render_separator):
        self.set_common_style = set_common_style
        self.render_separator = render_separator
        self.show_date_input = False
        self.date_input = {'day': '', 'month': '', 'year': ''}
        self.error_message = ""
        self.error_display_time = 0

    def render(self, date_manager):
        self.set_date_selector_window_position()
        self.set_common_style()
        self.begin_date_selector_window()
        self.render_input_date_toggle_button()
        if self.show_date_input:
            self.render_separator()
            self.render_date_input_fields(date_manager)
        self.end_date_selector_window()
        self.reset_style()

    def set_date_selector_window_position(self):
        imgui.set_next_window_position(191, 0)

    def begin_date_selector_window(self):
        window_flags = imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_AUTO_RESIZE
        imgui.begin("Date Selector", flags=window_flags)

    def render_input_date_toggle_button(self):
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.0, 0.5, 0.8, 1.0)
        if imgui.button("Input Date"):
            self.show_date_input = not self.show_date_input
        imgui.pop_style_color(1)

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

    def handle_date_confirmation(self, date_manager):
        try:
            if (self.date_input['day'] in ['', 'DD'] or
                self.date_input['month'] in ['', 'MM'] or
                self.date_input['year'] in ['', 'YYYY']):
                raise ValueError("Invalid date. Please enter a valid date.")

            day = int(self.date_input['day'])
            month = int(self.date_input['month'])
            year = int(self.date_input['year'])

            if year > 2050 or year < 2000:
                raise ValueError("Year must be between 2000 and 2050.")

            if not self.is_valid_date(year, month, day):
                raise ValueError("Invalid date. Please enter a valid date.")

            date_manager.set_date(month, day, year)
            self.show_date_input = False 
            self.error_message = ""  
        except ValueError as e:
            self.error_message = str(e)
            self.error_display_time = time.time()

    def is_valid_date(self, year, month, day):
        try:
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False
