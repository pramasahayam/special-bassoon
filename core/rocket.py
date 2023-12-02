from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

class Rocket:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.color = (1.0, 0.0, 0.0)  # Red color

    def update_position(self, trajectory_points, start_date, current_date, end_date):
        # Calculate the fraction of the journey completed
        journey_duration = end_date - start_date
        time_elapsed = current_date - start_date
        journey_fraction = time_elapsed / journey_duration

        # Find the appropriate point on the trajectory
        index = int(journey_fraction * len(trajectory_points))
        index = min(index, len(trajectory_points) - 1)  # Ensure index is within bounds
        self.position = trajectory_points[index]

    def render(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(*self.position)

        # Drawing the main body of the rocket as a cylinder
        gluCylinder(gluNewQuadric(), 0.5, 0.5, 2.0, 32, 32)

        # Drawing the cone of the rocket
        glTranslatef(0.0, 0.0, 2.0)
        glutSolidCone(0.5, 1.0, 32, 32)

        # Drawing fins (simple triangles)
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 0.5, 0.0)
        glVertex3f(-0.5, 0.5, -1.0)
        glVertex3f(0.5, 0.5, -1.0)
        glEnd()

        glPopMatrix()
