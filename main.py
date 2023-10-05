import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto 

# Constants for screen dimensions
WIDTH, HEIGHT = 800, 600

# Zooming and panning
LINEAR_ZOOM_AMOUNT = 100.0
dragging = False
last_mouse_x, last_mouse_y = 0, 0
INITIAL_CAMERA_DISTANCE = -1000
CAMERA_DISTANCE = INITIAL_CAMERA_DISTANCE
MIN_ZOOM_IN = -200
MAX_ZOOM_OUT = -5000

def draw_body(body, t):
    glColor3fv(body.color)
    quad = gluNewQuadric()
    slices, stacks = 100, 100
    glPushMatrix()
    x, y, z = body.compute_position(t)
    glTranslatef(x * 500, y * 500, z * 500)  # Adjusted scaling factor for visualization
    gluSphere(quad, body.radius, slices, stacks)
    glPopMatrix()

def main():
    global dragging, last_mouse_x, last_mouse_y, CAMERA_DISTANCE

    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

    gluPerspective(45, (display[0] / display[1]), 0.1, 5000.0)
    glTranslatef(0, 0, CAMERA_DISTANCE)

    sun = Sun()
    earth = Earth()
    mercury = Mercury()
    venus = Venus()
    mars = Mars()
    jupiter = Jupiter()
    saturn = Saturn()
    uranus = Uranus()
    neptune = Neptune()
    pluto = Pluto()
    space_bodies = [sun, earth, mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto]
    
    t = sun.ts.now()  # Initial time

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    return

                case pygame.MOUSEBUTTONDOWN:
                    match event.button:
                        case 1:
                            dragging = True
                            last_mouse_x, last_mouse_y = event.pos
                        case 4:  # Zooming in
                            new_distance = CAMERA_DISTANCE + LINEAR_ZOOM_AMOUNT
                            if new_distance <= MIN_ZOOM_IN:
                                CAMERA_DISTANCE = new_distance
                                glTranslatef(0, 0, LINEAR_ZOOM_AMOUNT)
                        case 5:  # Zooming out
                            new_distance = CAMERA_DISTANCE - LINEAR_ZOOM_AMOUNT
                            if new_distance >= MAX_ZOOM_OUT:
                                CAMERA_DISTANCE = new_distance
                                glTranslatef(0, 0, -LINEAR_ZOOM_AMOUNT)

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False

                case pygame.MOUSEMOTION:
                    if dragging:
                        mouse_x, mouse_y = event.pos
                        dx = mouse_x - last_mouse_x
                        dy = mouse_y - last_mouse_y
                        glTranslatef(dx * 0.5, -dy * 0.5, 0)
                        last_mouse_x, last_mouse_y = mouse_x, mouse_y

        t = sun.ts.tt(jd=t.tt + 0.1)  # Adjusting the time progression

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for body in space_bodies:
            draw_body(body, t)
        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == "__main__":
    main()
