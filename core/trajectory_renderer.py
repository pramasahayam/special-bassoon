import numpy as np
from OpenGL.GL import *

class TrajectoryRenderer:
    def __init__(self):
        self.trajectory_points = []

    def calculate_trajectory(self, origin_body, destination_body, current_time):
        # Use the compute_position method to get positions
        origin = origin_body.compute_position(current_time)
        destination = destination_body.compute_position(current_time)

        # Simple approximation of an elliptical orbit
        self.trajectory_points = self.generate_ellipse_points(origin, destination)

    def generate_ellipse_points(self, origin, destination):
        # Generate points on an ellipse
        points = []
        steps = 100
        for i in range(steps):
            t = np.linspace(0, 2 * np.pi, steps)
            x = (origin[0] + destination[0]) / 2 + (destination[0] - origin[0]) / 2 * np.cos(t)
            y = (origin[1] + destination[1]) / 2 + (destination[1] - origin[1]) / 2 * np.sin(t)
            z = np.zeros_like(x)  # Assuming in the XY plane
            points.append((x[i], y[i], z[i]))
        return points

    def render(self):
        glBegin(GL_LINE_STRIP)
        for point in self.trajectory_points:
            glVertex3f(*point)
        glEnd()
