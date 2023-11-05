from skyfield.api import load

class DateManager:
    def __init__(self):
        self.ts = load.timescale()
        self.current_date = self.ts.now()

    def set_date(self, month, day, year):
        self.current_date = self.ts.utc(year, month, day)

    def get_current_date(self):
        return self.current_date
