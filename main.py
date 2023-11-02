import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.solar_system import SolarSystem
from core.imgui_manager import ImGuiManager
from core.window_management import WindowManager
from core.user_interactions import UserInteractions

def main():
    window_manager = WindowManager()
    imgui_manager = ImGuiManager()
    solar_system = SolarSystem(window_manager, imgui_manager)
    user_interactions = UserInteractions(window_manager, imgui_manager)
    
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glEnable(GL_DEPTH_TEST)
    glTranslate(0, 0, solar_system.interactions.CAMERA_DISTANCE)
        
    while True:
        t = solar_system.space_bodies[0].ts.now()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle zooming, panning, and other user interactions
            user_interactions.handle_event(event, window_manager.resize)
            
            # Handle picking a planet and displaying its info box
            solar_system.handle_event(event, t)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Start ImGui frame
        imgui_manager.start_frame()
        
        # Drawing each celestial body
        for body in solar_system.space_bodies:
            solar_system.draw_body(body, t)
        
        # Render the ImGui UI
        imgui_manager.render_infobox(solar_system)

        imgui_manager.end_frame()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
