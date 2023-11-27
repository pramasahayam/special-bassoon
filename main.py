import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.solar_system import SolarSystem
from core.gui_manager import GuiManager
from core.window_manager import WindowManager
from core.user_interactions import UserInteractions
from core.date_manager import DateManager
from core.download_manager import DownloadManager

def main():

    window_manager = WindowManager()
    download_manager = DownloadManager()
    gui_manager = GuiManager(window_manager)

    # Disable resizing during the loading process
    window_manager.set_resizable(False)

    # Start asynchronous pre-download
    download_manager.pre_download_all_async()

    display_progress = 0.0
    while not download_manager.is_download_complete() or display_progress < 1.0:
        actual_progress = download_manager.get_download_progress()

        if actual_progress == 1.0:
            display_progress += 0.01
            display_progress = min(display_progress, 1.0)
        else:
            display_progress = actual_progress

        gui_manager.render_loading_screen(display_progress)

    # Re-enable window resizing after the loading is complete
    window_manager.set_resizable(True)

    user_interactions = UserInteractions(window_manager, gui_manager)
    date_manager = DateManager()
    solar_system = SolarSystem(window_manager, user_interactions)
    
    glEnable(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glEnable(GL_DEPTH_TEST)
    glTranslate(0, 0, solar_system.interactions.CAMERA_DISTANCE)
    
    while True:
        t = date_manager.get_current_date()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            gui_manager.process_event(event)

            # Only process other interactions if ImGui is not being used
            if not gui_manager.is_imgui_hovered() and not gui_manager.is_imgui_used():
                user_interactions.handle_event(event)
                solar_system.handle_event(event, t)
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        gui_manager.start_frame()
        
        # Drawing the skybox
        solar_system.draw_skybox(solar_system.skybox_texture_id)

        # Drawing each celestial body
        for body in solar_system.space_bodies:
            solar_system.draw_body(body, t)
        
        gui_manager.render_ui(solar_system, date_manager, user_interactions)

        gui_manager.end_frame()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()