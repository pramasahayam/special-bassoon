import numpy as np
from OpenGL.GL import *
import numpy as np

class TrajectoryPlotter:
    def __init__(self, space_bodies):
        self.space_bodies = space_bodies  # List of all celestial bodies

    def calculate_trajectory(self, origin_index, destination_index, num_points=100):
        """
        Calculate the trajectory path between two celestial bodies.
        This is a simplified example that creates a straight-line path.
        Replace with your specific trajectory calculation.
        """
        origin = self.space_bodies[origin_index]
        destination = self.space_bodies[destination_index]

        # Simple straight line for demonstration
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            x = origin.position[0] * (1 - t) + destination.position[0] * t
            y = origin.position[1] * (1 - t) + destination.position[1] * t
            z = origin.position[2] * (1 - t) + destination.position[2] * t
            points.append((x, y, z))

        return points

    def render_trajectory(self, points):
        """
        Render the trajectory using OpenGL.
        Connects the points using a line strip.
        """
        glBegin(GL_LINE_STRIP)
        for x, y, z in points:
            glVertex3f(x, y, z)
        glEnd()
