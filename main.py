import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from space_bodies import Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto 
from core.window_management import WindowManager
from core.solar_system import SolarSystem

def main():
    window = WindowManager()
    glTranslate(0, 0, -5000)  # Initialize camera distance; this can be moved to a constant for clarity.

    # Instantiate the space bodies
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

    solar_system = SolarSystem(space_bodies, window.screen)

    t = sun.ts.now()  # Current time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            solar_system.handle_event(event, window.resize, t)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        solar_system.render(t)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
