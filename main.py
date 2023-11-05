import pygame
import imgui
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.solar_system import SolarSystem
from core.gui_manager import GuiManager
from core.window_manager import WindowManager
from core.user_interactions import UserInteractions
from core.date_manager import DateManager

def main():
    window_manager = WindowManager()
    gui_manager = GuiManager()
    solar_system = SolarSystem(window_manager, gui_manager)
    user_interactions = UserInteractions(window_manager, gui_manager)
    
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glEnable(GL_DEPTH_TEST)
    glTranslate(0, 0, solar_system.interactions.CAMERA_DISTANCE)
  
    date_manager = DateManager()
    
    while True:
        t = date_manager.get_current_date()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            gui_manager.process_event(event)

            # Handle zooming, panning, and other user interactions
            user_interactions.handle_event(event, window_manager.resize)
            
            # Handle picking a planet and displaying its info box
            solar_system.handle_event(event, t)
              
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        gui_manager.start_frame()
        
        # Drawing the skybox
        solar_system.draw_skybox(solar_system.skybox_texture_id)

        # Drawing each celestial body
        for body in solar_system.space_bodies:
            solar_system.draw_body(body, t)
            if not body.orbital_center:
                gui_manager.render_labels(body, t)
        
        gui_manager.render_ui(solar_system, date_manager, user_interactions)

        gui_manager.end_frame()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
