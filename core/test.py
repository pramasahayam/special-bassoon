#from imgui_manager
import core.buttons as button

class center_button:
    def __init__(self):
        
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.camera_position = self.width/2, self.height/2
        self.initial_position = self.width/2, self.height/2
                
    def center_on_sun(self):
        self.camera_position[0] = self.initial_position[0]
        self.camera_position[1] = self.initial_position[1]
 
 #from solar_system
                         
        #center button
        # Define the size and position of the ImGui window for the button
        button_size = (150, 50)
        center_button.initial_position = pygame.display.Info().current_w/2, pygame.display.Info().current_h/2
        center_button.width = pygame.display.Info().current_w
        center_button.height = pygame.display.Info().current_h
        button_position = (center_button.initial_position[0], center_button.initial_position[1])

        # Set the window position to the bottom right
        window_pos_x = center_button.initial_position[0] + center_button.width - button_size[0]
        window_pos_y = center_button.initial_position[1] + center_button.height - button_size[1]

        # Create the ImGui window
        imgui.set_next_window_position(window_pos_x, window_pos_y)
        imgui.set_next_window_size(button_size[0], button_size[1])
        imgui.begin("Button Window", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE)

        if imgui.button("Center Camera"):
            center_button.center_on_sun()