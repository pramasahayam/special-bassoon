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
        r1 = origin_body
        r2 = destination_body

        # Get delta-v and transfer time from the calculator
        # Assuming that the hohmann_transfer method requires the gravitational parameter (mu) and radii (r1, r2)
        total_deltav, transfer_time = self.delta_v_calculator.hohmann_transfer(origin_body.mu, r1.semimajoraxis, r2.semimajoraxis)

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
        major_axis_length = (r1.semimajoraxis + r2.semimajoraxis) / 2

        # Minor axis length adjusted by minor_axis_factor
        minor_axis_length = major_axis_length * minor_axis_factor

        # Normalize the vector for calculating points
        vector = np.array(destination_pos) - np.array(origin_pos)
        unit_vector = vector / major_axis_length

        # Normal vector for the minor axis displacement
        normal_vector = np.cross(unit_vector, [0, 0, 1])
        normal_vector /= np.linalg.norm(normal_vector)

        origin_radius = r1.radius
        destination_radius = r2.radius

        for i in range(steps):
            angle = 2 * np.pi * i / steps

            adjusted_minor_axis_length = self.adjust_minor_axis(minor_axis_length, angle, origin_radius, destination_radius)

            # Calculate the point on the major axis
            major_axis_disp = major_axis_length * np.cos(angle) / 2

            # Calculate the point on the minor axis
            minor_axis_disp = adjusted_minor_axis_length * np.sin(angle)

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

            point = self.calculate_3d_point(center_x, center_y, major_axis_disp, minor_axis_disp, unit_vector, normal_vector, angle, origin_pos, destination_pos)
            points.append(tuple(point))

        return points

    def calculate_3d_point(self, center_x, center_y, major_axis_disp, minor_axis_disp, unit_vector, normal_vector, angle, origin_pos, destination_pos):
        # Calculate the 3D point and apply z-coordinate interpolation
        point = [center_x + major_axis_disp * unit_vector[0],
                 center_y + major_axis_disp * unit_vector[1],
                 origin_pos[2]]  # Start with the z-coordinate of the origin
        point += minor_axis_disp * normal_vector

        # Apply z-coordinate interpolation
        z_interp = (np.cos(angle) + 1) / 2  # Adjusted interpolation logic
        point[2] = origin_pos[2] * (1 - z_interp) + destination_pos[2] * z_interp

        return point

    def offset_point_from_body(self, point, origin_pos, destination_pos, origin_radius, destination_radius):
        # Calculate the distance from the point to each celestial body
        distance_to_origin = np.linalg.norm(np.array(point) - np.array(origin_pos))
        distance_to_destination = np.linalg.norm(np.array(point) - np.array(destination_pos))

        # Adjust the point position if it's within the radius of the celestial bodies
        if distance_to_origin < origin_radius:
            # Implement logic to adjust the point position
            point = self.adjust_point_position(point, origin_pos, origin_radius)
        if distance_to_destination < destination_radius:
            # Implement logic to adjust the point position
            point = self.adjust_point_position(point, destination_pos, destination_radius)

        return point

    def adjust_point_position(self, point, body_pos, body_radius):
        # Calculate a safe position for the point, considering the body's radius
        direction = np.array(point) - np.array(body_pos)
        direction /= np.linalg.norm(direction)  # Normalize the direction vector
        safe_distance = body_radius + 0.1  # Add a small buffer distance
        adjusted_point = np.array(body_pos) + direction * safe_distance
        return adjusted_point.tolist()

    def adjust_minor_axis(self, minor_axis_length, angle, origin_radius, destination_radius):
        if angle < np.pi / 2 or angle > 3 * np.pi / 2:
            return minor_axis_length + origin_radius
        elif np.pi / 2 <= angle <= 3 * np.pi / 2:
            return minor_axis_length + destination_radius
        else:
            return minor_axis_length

    def render(self):
        if self.should_render:
            glPushMatrix()  # Save the current OpenGL state
            glLineWidth(2)
            glBegin(GL_LINE_STRIP)
            for point in self.trajectory_points:
                glColor3f(0.0, 1.0, 0.0)  # Green color for trajectory
                glVertex3f(*point)
            glEnd()

            # Reset color to default (white) after rendering the trajectory
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(1)
            
            glPopMatrix()  # Restore the previous OpenGL state

    def render_markers(self):
        marker_interval = len(self.trajectory_points) // 10  # Place markers at intervals
        for i in range(0, len(self.trajectory_points), marker_interval):
            if i + marker_interval < len(self.trajectory_points):
                self.render_arrow(self.trajectory_points[i], self.trajectory_points[i + marker_interval])

    def render_arrow(self, start_point, end_point):
        glColor3f(1.0, 0.0, 0.0)  # Red color for arrows
        glPushMatrix()
        glTranslatef(*start_point)
        direction = np.array(end_point) - np.array(start_point)
        direction /= np.linalg.norm(direction)
        arrow_length = 0.5  # Set the arrow length

        # Render arrow shaft
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(*(direction * arrow_length))
        glEnd()

        # Render arrowhead
        arrowhead_size = 0.1  # Set arrowhead size
        glBegin(GL_TRIANGLES)
        for angle in np.linspace(0, 2 * np.pi, 3, endpoint=False):  # Triangle for arrowhead
            dx = arrowhead_size * np.cos(angle)
            dy = arrowhead_size * np.sin(angle)
            glVertex3f(*(direction * arrow_length + np.array([dx, dy, 0])))
        glEnd()
        glPopMatrix()