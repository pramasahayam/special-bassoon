import datetime
from skyfield.api import load

class DateManager:
    def __init__(self):
        self.ts = load.timescale()
        self.current_date = self.ts.now()

    def calculate_transfer_time(self, origin_body, destination_body):
        # For simplicity, return a fixed transfer time of 10 days
        transfer_time_in_days = 10
        return transfer_time_in_days * 86400  # Convert days to seconds
    
    def add_days(self, days):
        self.current_date = self.current_date.utc_jpl() + datetime.timedelta(days=days)

    def progress_time(self):
        # Progress time by a fraction of a day each frame
        # Assuming a 10-day journey, divided into 2400 parts (10 days * 24 hours * 10 increments per hour)
        time_increment = datetime.timedelta(days=1/2400)
        self.current_date += time_increment

        # Optional: Add logic to stop time progression after 10 days

    def get_current_date(self):
        return self.current_date

    def set_date(self, month, day, year):
        self.current_date = self.ts.utc(year, month, day)

    
