import pygame
import imgui
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.solar_system import SolarSystem
from core.gui_manager import GuiManager

def main():
    solar_system = SolarSystem()
    glTranslate(0, 0, solar_system.interactions.CAMERA_DISTANCE)
    gui_manager = GuiManager()
    solar_system.set_imgui_manager(gui_manager)
    
    while True:
        t = solar_system.space_bodies[0].ts.now()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            gui_manager.process_event(event)
            
            # Handle zooming, panning, and other user interactions
            solar_system.interactions.handle_event(event, solar_system.window.resize)
              
            # Handle picking a planet and displaying its info box
            solar_system.handle_event(event, t)
              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Start ImGui frame
        gui_manager.start_frame(solar_system.window.screen)
        
        # Drawing each celestial body
        for body in solar_system.space_bodies:
            solar_system.draw_body(body, t)

        # Render the info boxes for celestial bodies
        solar_system.render_ui()

        # Render the button on top of everything 
        gui_manager.render_ui()

        gui_manager.end_frame()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
