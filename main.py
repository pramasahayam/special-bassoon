import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from space_bodies import Sun

# Constants for screen dimensions
WIDTH, HEIGHT = 800, 600

# Zooming and panning
LINEAR_ZOOM_AMOUNT = 200.0
dragging = False
last_mouse_x, last_mouse_y = 0, 0
INITIAL_CAMERA_DISTANCE = -1000
CAMERA_DISTANCE = INITIAL_CAMERA_DISTANCE
MIN_ZOOM_IN = -160

def screen_to_world(x, y):
    """Convert screen coordinates to world coordinates."""
    y = HEIGHT - y  # flip the y-coordinate
    z = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    return gluUnProject(x, y, z)

def draw_sun(sun):
    glColor3fv(sun.color)
    quad = gluNewQuadric()
    slices, stacks = 100, 100
    glPushMatrix()
    gluSphere(quad, sun.radius, slices, stacks)
    glPopMatrix()

def main():
    global dragging, last_mouse_x, last_mouse_y, CAMERA_DISTANCE

    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 5000.0)
    glTranslatef(0, 0, CAMERA_DISTANCE)

    sun = Sun()
    sun.radius = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse_x, last_mouse_y = event.pos
                elif event.button == 4:  # Zooming in
                    new_distance = CAMERA_DISTANCE + LINEAR_ZOOM_AMOUNT
                    if new_distance <= -200:  # Make sure we don't zoom in past -200
                        CAMERA_DISTANCE = new_distance
                        glTranslatef(0, 0, LINEAR_ZOOM_AMOUNT)

                elif event.button == 5:  # Zooming out
                    new_distance = CAMERA_DISTANCE - LINEAR_ZOOM_AMOUNT
                    if new_distance >= -5000:  # Make sure we don't zoom out past -5000
                        CAMERA_DISTANCE = new_distance
                        glTranslatef(0, 0, -LINEAR_ZOOM_AMOUNT)


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - last_mouse_x
                dy = mouse_y - last_mouse_y
                glTranslatef(dx * 0.5, -dy * 0.5, 0)
                last_mouse_x, last_mouse_y = mouse_x, mouse_y

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_sun(sun)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()