from core.deltav_calculator import DeltaVCalculator
import numpy as np
from OpenGL.GL import *

class TrajectoryPlotter:
    def __init__(self, space_bodies, date_manager):
        self.space_bodies = space_bodies
        self.date_manager = date_manager
        self.delta_v_calculator = DeltaVCalculator(space_bodies)
        self.trajectory_points = None

    def calculate_trajectory(self, origin_index, destination_index, num_points=100):
        if origin_index >= len(self.space_bodies) or destination_index >= len(self.space_bodies):
            return [], 0, 0

        try:
            origin = self.space_bodies[origin_index]
            destination = self.space_bodies[destination_index]

            current_date = self.date_manager.get_current_date()
            origin_position = origin.compute_position(current_date)
            destination_position = destination.compute_position(current_date)

            r1 = np.linalg.norm(origin_position)
            r2 = np.linalg.norm(destination_position)
            total_deltav, transfer_time_conversions = self.delta_v_calculator.hohmann_transfer(origin_index, r1, r2)
            a_transfer = (r1 + r2) / 2

            b_transfer = a_transfer * 0.5  # Approximation for visualization

            points = []
            for i in range(num_points):
                angle = 2 * np.pi * i / num_points
                x = a_transfer * np.cos(angle)
                y = b_transfer * np.sin(angle)
                z = 0

                points.append((x, y, z))

            self.trajectory_points = points
            return points, total_deltav, transfer_time_conversions[3]
        except Exception:
            return [], 0, 0

    def render_trajectory(self):
        if self.trajectory_points:
            glBegin(GL_LINE_STRIP)
            for x, y, z in self.trajectory_points:
                glVertex3f(x, y, z)
            glEnd()

    def set_trajectory_points(self, points):
        self.trajectory_points = points
