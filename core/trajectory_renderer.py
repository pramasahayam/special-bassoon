import numpy as np
from OpenGL.GL import *

class TrajectoryRenderer:
    def __init__(self):
        self.trajectory_points = []
        self.should_render = False

    def calculate_trajectory(self, origin_body, destination_body, current_time):
        print("Calculating trajectory...")  # Debug statement
        origin = origin_body.compute_position(current_time)
        destination = destination_body.compute_position(current_time)
        self.trajectory_points = self.generate_ellipse_points(origin, destination)
        self.should_render = True
        print(f"Trajectory points: {self.trajectory_points[:5]}")  # Print first few points for debug

    def render(self):
        if self.should_render:
            print("Rendering trajectory...")  # Debug statement
            glBegin(GL_LINE_STRIP)
            for point in self.trajectory_points:
                glVertex3f(*point)
            glEnd()

    def generate_ellipse_points(self, origin, destination):
        # Generate ellipse points
        points = []
        steps = 100
        for i in range(steps):
            t = np.linspace(0, 2 * np.pi, steps)
            x = (origin[0] + destination[0]) / 2 + (destination[0] - origin[0]) / 2 * np.cos(t)
            y = (origin[1] + destination[1]) / 2 + (destination[1] - origin[1]) / 2 * np.sin(t)
            z = np.zeros_like(x)  # Assuming in the XY plane
            points.append((x[i], y[i], z[i]))
        return points

    def reset_render(self):
        self.should_render = False
