import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui

class LoadingScreen:
    def __init__(self, window_manager, gui_manager):
        self.window_manager = window_manager
        self.gui_manager = gui_manager
        self.skybox_texture_id = self.load_texture("textures/misc/loading_texture.png")
        self.overlay_texture_id = self.load_texture("textures/misc/team_logo.png")

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

    def draw_overlay(self, overlay_texture_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, overlay_texture_id)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.window_manager.WIDTH, 0, self.window_manager.HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glBegin(GL_QUADS)
        # Adjust these texture coordinates if the texture is mirrored
        glTexCoord2f(0, 0); glVertex2f(0, 0)  # Bottom-left corner
        glTexCoord2f(1, 0); glVertex2f(self.window_manager.WIDTH, 0)  # Bottom-right corner
        glTexCoord2f(1, 1); glVertex2f(self.window_manager.WIDTH, self.window_manager.HEIGHT)  # Top-right corner
        glTexCoord2f(0, 1); glVertex2f(0, self.window_manager.HEIGHT)  # Top-left corner
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

    def render_progress_bar(self, progress):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(self.window_manager.WIDTH, self.window_manager.HEIGHT/6)
        self.gui_manager.set_common_style()
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

        # Start the ImGui frame
        self.gui_manager.start_frame()

        # Render the progress bar using ImGui
        self.render_progress_bar(progress)

        # End the ImGui frame
        self.gui_manager.end_frame()

        # Enable blending for transparent texture
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Render the overlay image
        self.draw_overlay(self.overlay_texture_id)

        # Disable blending if it's not needed for the rest of your rendering
        glDisable(GL_BLEND)

        # Update the display
        pygame.display.flip()
