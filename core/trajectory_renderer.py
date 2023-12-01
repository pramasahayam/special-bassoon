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
        
        normalization_factor = 10000

        origin_pos = origin_body.compute_position(current_time)
        destination_pos = destination_body.compute_position(current_time)

        # Use the semi-major axis of each body for r1 and r2
        r1 = origin_body.semimajoraxis
        r2 = destination_body.semimajoraxis

        # Get delta-v and transfer time from the calculator
        # Assuming that the hohmann_transfer method requires the gravitational parameter (mu) and radii (r1, r2)
        total_deltav, transfer_time = self.delta_v_calculator.hohmann_transfer(origin_body.mu, r1, r2)

        # Adjust the minor axis based on the delta-v
        minor_axis_factor = total_deltav / normalization_factor  # Adjust this factor as needed

        self.trajectory_points = self.generate_ellipse_points(origin_pos, destination_pos, r1, r2, minor_axis_factor)
        self.should_render = True

    def generate_ellipse_points(self, origin_pos, destination_pos, r1, r2, minor_axis_factor):
        points = []
        steps = 100

        # Calculate the midpoint (center) for the x and y coordinates
        center_x, center_y = (np.array(origin_pos) + np.array(destination_pos))[:2] / 2

        # Major axis length could be based on r1 and r2
        major_axis_length = (r1 + r2) / 2

        # Minor axis length adjusted by minor_axis_factor
        minor_axis_length = major_axis_length * minor_axis_factor

        # Normalize the vector for calculating points
        vector = np.array(destination_pos) - np.array(origin_pos)
        unit_vector = vector / major_axis_length

        # Normal vector for the minor axis displacement
        normal_vector = np.cross(unit_vector, [0, 0, 1])
        normal_vector /= np.linalg.norm(normal_vector)

        for i in range(steps):
            angle = 2 * np.pi * i / steps

            # Calculate the point on the major axis
            major_axis_disp = major_axis_length * np.cos(angle) / 2

            # Calculate the point on the minor axis
            minor_axis_disp = minor_axis_length * np.sin(angle)

            # Combine the displacements to get the 3D point
            point = [center_x + major_axis_disp * unit_vector[0],
                    center_y + major_axis_disp * unit_vector[1],
                    origin_pos[2]]  # Start with the z-coordinate of the origin
            point += minor_axis_disp * normal_vector

            # Invert the z-coordinate interpolation logic
            if angle <= np.pi:
                # From 0 to π, interpolate from destination's depth to origin's depth
                z_interp = angle / np.pi
            else:
                # From π to 2π, interpolate back from origin's depth to destination's depth
                z_interp = (2 * np.pi - angle) / np.pi

            point[2] = destination_pos[2] + (origin_pos[2] - destination_pos[2]) * z_interp

            points.append(tuple(point))

        return points

    def render(self):
        if self.should_render:
            glBegin(GL_POINTS)  # Or GL_LINES
            for point in self.trajectory_points:
                glVertex3f(*point)
            glEnd()
