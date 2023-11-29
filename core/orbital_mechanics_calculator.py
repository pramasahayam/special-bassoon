from astropy import units as u
from poliastro.bodies import Sun, Earth, Mars, Venus, Mercury, Jupiter, Saturn, Uranus, Neptune, Pluto
from poliastro.maneuver import Maneuver
from poliastro.twobody import Orbit
from astropy.time import Time
import datetime
import numpy as np

class OrbitalMechanicsCalculator:
    def __init__(self, date_manager):
        self.date_manager = date_manager
        self.bodies = {
            "Sun": Sun,
            "Earth": Earth,
            "Mars": Mars,
            "Venus": Venus,
            "Mercury": Mercury,
            "Jupiter": Jupiter,
            "Saturn": Saturn,
            "Uranus": Uranus,
            "Neptune": Neptune,
            "Pluto": Pluto
        }

    def calculate_transfer_orbit(self, origin_name, destination_name, transfer_time_days):
        if origin_name not in self.bodies or destination_name not in self.bodies:
            raise ValueError("Invalid celestial body name.")

        origin_body = self.bodies[origin_name]
        destination_body = self.bodies[destination_name]

        departure_date = self.date_manager.get_current_date().utc_datetime()
        arrival_date = departure_date + datetime.timedelta(days=transfer_time_days)

        ss_origin = Orbit.from_body_ephem(origin_body, Time(departure_date))
        ss_destination = Orbit.from_body_ephem(destination_body, Time(arrival_date))

        man = Maneuver.hohmann(ss_origin, ss_destination.a)
        ss_trans, ss_final = ss_origin.apply_maneuver(man, intermediate=True)

        num_points = 100  # Number of points in the trajectory
        start_time = Time(departure_date)
        end_time = Time(arrival_date)
        total_duration = (end_time - start_time).to(u.day)  # Duration of the transfer in days
        step = total_duration / num_points  # Duration of each step in days

        trajectory_points = []
        for i in range(num_points):
            # Calculate the time of flight for this step
            time_of_flight = step * i
            # Propagate the orbit to this time of flight
            r, v = ss_trans.propagate(time_of_flight).rv()
            trajectory_points.append(r.value)  # Use the position vector as-is

        return trajectory_points
