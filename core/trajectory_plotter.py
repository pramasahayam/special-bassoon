import numpy as np
from OpenGL.GL import *
from core.orbital_mechanics_calculator import OrbitalMechanicsCalculator

class TrajectoryPlotter:
    def __init__(self, space_bodies, date_manager, distance_scale):
        self.space_bodies = space_bodies
        self.date_manager = date_manager
        self.orbital_calculator = OrbitalMechanicsCalculator(date_manager)
        self.trajectory_points = None
        self.DISTANCE_SCALE = distance_scale  # Scaling factor for distance

    def calculate_trajectory(self, origin_name, destination_name):
        transfer_time_days = 180  # Default transfer time in days
        raw_points = self.orbital_calculator.calculate_transfer_orbit(
            origin_name, destination_name, transfer_time_days
        )

        # Scale down the trajectory points to match the solar system scale
        self.trajectory_points = [point / self.DISTANCE_SCALE for point in raw_points]

    def render_trajectory(self):
        if self.trajectory_points:
            glBegin(GL_LINE_STRIP)
            for x, y, z in self.trajectory_points:
                glVertex3f(x, y, z)
            glEnd()

    def set_trajectory_points(self, points):
        self.trajectory_points = points

