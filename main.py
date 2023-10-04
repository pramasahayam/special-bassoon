import pygame
from math import cos, sin, radians
from space_bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Lua

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 1200
BACKGROUND_COLOR = (0, 0, 0)
TIME_SCALE = 1/365.25  # Adjust this for real-time simulation

# Create screen and clock for controlling frame rate
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

class SpaceApp:
    def __init__(self):
        # Initialize celestial bodies
        self.sun = Sun(800, 400)
        self.mercury = Mercury(860, 400)
        self.venus = Venus(920, 400)
        self.earth = Earth(980, 400)
        self.mars = Mars(1040, 400)
        self.jupiter = Jupiter(1100, 400)
        self.saturn = Saturn(1160, 400)
        self.uranus = Uranus(1220, 400)
        self.neptune = Neptune(1280, 400)
        self.pluto = Pluto(1340, 400)
        self.lua = Lua(self.earth.x + 30, self.earth.y)
        
        self.bodies = [self.mercury, self.venus, self.earth, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.lua]

        # Dictionary to store individual angles for each space body
        self.angles = {
            body: 0 for body in self.bodies
        }

        # Calculate and store initial orbit radii
        self.orbit_radii = {
            body: ((self.sun.x - body.x) ** 2 + (self.sun.y - body.y) ** 2) ** 0.5 for body in self.bodies if body != self.lua
        }
        self.orbit_radii[self.lua] = ((self.earth.x - self.lua.x) ** 2 + (self.earth.y - self.lua.y) ** 2) ** 0.5

    def draw_space_body(self, body):
        pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

    def rotate_space_body(self, body, center_body):
        orbit_radius = self.orbit_radii[body]  # Fetch the orbit radius from the precomputed values
        
        # Angle increments based on the orbital period of each space body
        angle_increment = (360 / body.rotation_period) * TIME_SCALE

        # Update angle for the current space body
        self.angles[body] += angle_increment

        body.x = center_body.x + orbit_radius * cos(radians(self.angles[body]))
        body.y = center_body.y + orbit_radius * sin(radians(self.angles[body]))

    def run(self):
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)
            
            # Draw the sun first
            self.draw_space_body(self.sun)

            # Rotate and draw planets
            for body in self.bodies:
                if body != self.lua:  # Lua will rotate around Earth
                    self.rotate_space_body(body, self.sun)
                else:
                    self.rotate_space_body(body, self.earth)  # Lua rotates around Earth
                self.draw_space_body(body)

            pygame.display.flip()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

if __name__ == "__main__":
    app = SpaceApp()
    app.run()
    pygame.quit()