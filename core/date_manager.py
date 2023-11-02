class DateManager:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.current_date = self.solar_system.space_bodies[0].ts.now()

    def set_date(self, new_date_str):
        # Parse the new date string and update the current_date
        # This is where you would use Skyfield to parse the date string and update self.current_date
        pass

    def get_current_date(self):
        return self.current_date
