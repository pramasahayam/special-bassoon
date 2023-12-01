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

        # Calculate the center and the vector from the origin to the destination
        vector = np.array(destination_pos) - np.array(origin_pos)
        center = np.array(origin_pos) + vector / 2

        # Major axis length is the distance between the origin and destination
        major_axis_length = np.linalg.norm(vector)

        # Minor axis length (can be adjusted for visualization)
        minor_axis_length = major_axis_length * 0.5

        # Normalize the vector for calculating points
        unit_vector = vector / major_axis_length

        # Normal vector for the minor axis displacement
        normal_vector = np.cross(unit_vector, [0, 0, 1])
        if np.linalg.norm(normal_vector) != 0:
            normal_vector /= np.linalg.norm(normal_vector)

        for i in range(steps):
            angle = 2 * np.pi * i / steps

            # Calculate the point on the major axis
            major_axis_disp = major_axis_length * np.cos(angle) / 2

            # Calculate the point on the minor axis
            minor_axis_disp = minor_axis_length * np.sin(angle)

            # Combine the displacements to get the 3D point
            point = center + major_axis_disp * unit_vector
            point += minor_axis_disp * normal_vector

            # Adjust the z-coordinate to vary linearly from origin to destination
            z_interp = (1 - np.cos(angle)) / 2  # Ranges from 0 at origin to 1 at destination
            point[2] = origin_pos[2] * (1 - z_interp) + destination_pos[2] * -z_interp

            points.append(tuple(point))

        return points

    def render(self):
        if self.should_render:
            glBegin(GL_POINTS)  # Or GL_LINES
            for point in self.trajectory_points:
                glVertex3f(*point)
            glEnd()
