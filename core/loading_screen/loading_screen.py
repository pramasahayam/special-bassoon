import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui

class LoadingScreen:
    def __init__(self, window_manager, gui_manager):
        self.window_manager = window_manager
        self.gui_manager = gui_manager
        self.skybox_texture_id = self.load_texture("textures/misc/loading_texture.png")
        self.logo_texture_id = self.load_texture("textures/misc/team_logo.png")

    def load_texture(self, texture_path):
        texture_surface = pygame.image.load(texture_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        return texture_id

    def draw_skybox(self):
        size = 300000
        vertices = [
            [-size, -size, -size], [size, -size, -size], [size, size, -size], [-size, size, -size],
            [-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]
        ]

        tex_coords = [
            [0.25, 0.333], [0.5, 0.333], [0.5, 0.666], [0.25, 0.666],
            [0.0, 0.333], [0.75, 0.333], [0.75, 0.666], [1.0, 0.666]
        ]

        indices = [
            [1, 2, 3, 0], [2, 6, 7, 3], [7, 4, 0, 3], [4, 5, 1, 0], [5, 6, 2, 1], [6, 5, 4, 7]
        ]

        glDepthMask(GL_FALSE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.skybox_texture_id)

        for face in indices:
            glBegin(GL_QUADS)
            for i, vertex in enumerate(face):
                glTexCoord2f(tex_coords[vertex][0], tex_coords[vertex][1])
                glVertex3fv(vertices[vertex])
            glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDepthMask(GL_TRUE)

    def blit_logo(self):
        width, height = self.window_manager.get_current_dimensions()

        # Assuming the logo is square and you want it to be 200x200 pixels
        logo_size = 200
        logo_x = (width - logo_size) / 2
        logo_y = (height - logo_size) / 2

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.logo_texture_id)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(logo_x, logo_y)
        glTexCoord2f(1, 0); glVertex2f(logo_x + logo_size, logo_y)
        glTexCoord2f(1, 1); glVertex2f(logo_x + logo_size, logo_y + logo_size)
        glTexCoord2f(0, 1); glVertex2f(logo_x, logo_y + logo_size)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        
    def render_progress_bar(self, progress):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.window_manager.WIDTH, self.window_manager.HEIGHT/6)
        imgui.begin("Download Progress", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_SCROLLBAR)

        imgui.text("Downloading Ephemeris Data...")
        imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, 0.0, 0.5, 0.8, 1.0)
        imgui.progress_bar(progress)
        imgui.pop_style_color(1)

        percentage = int(progress * 100)
        imgui.text(f"Progress: {percentage}%")

        imgui.end()

    def render(self, progress):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.draw_skybox()
        self.blit_logo()

        self.gui_manager.start_frame()
        self.render_progress_bar(progress)
        self.gui_manager.end_frame()
        pygame.display.flip()
