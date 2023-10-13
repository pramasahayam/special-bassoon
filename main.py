import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.solar_system import SolarSystem

def main():
    pygame.init()
    solar_system = SolarSystem()

    glTranslate(0, 0, solar_system.interactions.CAMERA_DISTANCE)

    while True:
        t = solar_system.space_bodies[0].ts.now()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle zooming, panning, and other user interactions
            solar_system.interactions.handle_event(event, solar_system.window.resize)
            
            # Handle picking a planet and displaying its info box
            solar_system.handle_event(event, t)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Drawing each space body
        for body in solar_system.space_bodies:
            solar_system.draw_body(body, t)
        
        # Render the Pygame UI
        solar_system.render_ui()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
 