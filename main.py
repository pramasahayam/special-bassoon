import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto 
from core.user_interactions import UserInteractions
from core.window_management import WindowManager

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
    window = WindowManager()
    interactions = UserInteractions()
    glTranslate(0, 0, interactions.CAMERA_DISTANCE)

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
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            interactions.handle_event(event, window.resize)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for body in space_bodies:
            draw_body(body, t) 
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
