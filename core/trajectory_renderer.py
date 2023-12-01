import numpy as np
from OpenGL.GL import *

class TrajectoryRenderer:
    def __init__(self, delta_v_calculator=None):
        self.delta_v_calculator = delta_v_calculator
        self.trajectory_points = []
        self.should_render = False

    def set_delta_v_calculator(self, delta_v_calculator):
        self.delta_v_calculator = delta_v_calculator

    def calculate_trajectory(self, origin_body, destination_body, current_time):
        if not self.delta_v_calculator:
            print("DeltaVCalculator not set. Cannot calculate trajectory.")
            return

        origin_pos = origin_body.compute_position(current_time)
        destination_pos = destination_body.compute_position(current_time)

        print(f"Origin Position: {origin_pos}")
        print(f"Destination Position: {destination_pos}")

        r1 = np.linalg.norm(origin_pos)
        r2 = np.linalg.norm(destination_pos)
        a_transfer = (r1 + r2) / 2
        self.trajectory_points = self.generate_ellipse_points(origin_pos, destination_pos, a_transfer)
        self.should_render = True

    def generate_ellipse_points(self, origin_pos, destination_pos, a_transfer):
        points = []
        steps = 100
        center = (np.array(origin_pos) + np.array(destination_pos)) / 2
        major_axis = np.array(destination_pos) - np.array(origin_pos)
        minor_axis_length = np.sqrt(a_transfer**2 - np.linalg.norm(major_axis)**2 / 4)

        for i in range(steps):
            angle = 2 * np.pi * i / steps
            x = center[0] + a_transfer * np.cos(angle)
            y = center[1] + minor_axis_length * np.sin(angle)
            z = center[2]  # Assuming the orbit lies in the plane of the two bodies

            points.append((x, y, z))

        print(f"Sample Ellipse Points: {points[:5]}")  # Print the first few points

        return points

    def render(self):
        if self.should_render:
            glBegin(GL_POINTS)  # Or GL_LINES
            for point in self.trajectory_points:
                glVertex3f(*point)
            glEnd()
