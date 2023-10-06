import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto 

# Zooming and panning parameters
LINEAR_ZOOM_AMOUNT = 100.0
dragging = False
last_mouse_x, last_mouse_y = 0, 0
INITIAL_CAMERA_DISTANCE = -1000
CAMERA_DISTANCE = INITIAL_CAMERA_DISTANCE
MIN_ZOOM_IN = -200
MAX_ZOOM_OUT = -5000

def resize(WIDTH, HEIGHT):
    """Handles the window resize."""
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 10000.0)
    glMatrixMode(GL_MODELVIEW)

def draw_body(body, t):
    glColor3fv(body.color)
    quad = gluNewQuadric()
    slices, stacks = 100, 100
    glPushMatrix()
    x, y, z = body.compute_position(t)
    glTranslatef(x * 1000, y * 1000, z * 1000)  # Scaling factor for visualization
    gluSphere(quad, body.radius, slices, stacks)
    glPopMatrix()

def main():
    global dragging, last_mouse_x, last_mouse_y, CAMERA_DISTANCE

    pygame.init()
    # Set screen dimensions to the system's dimensions
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL | pygame.RESIZABLE)
    pygame.display.set_caption('Solar System Simulation')
    resize(WIDTH, HEIGHT)  # Adjust the viewport and aspect ratio
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

    t = sun.ts.now()  # Current time

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    return

                case pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.size
                    resize(WIDTH, HEIGHT)

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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for body in space_bodies:
            draw_body(body, t)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
