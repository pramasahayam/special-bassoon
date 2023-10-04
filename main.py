import pygame
from math import cos, sin, radians
from space_bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Lua

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1600, 1200
BACKGROUND_COLOR = (0, 0, 0)

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
        
        self.bodies = [self.sun, self.mercury, self.venus, self.earth, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.pluto, self.lua]
        self.angle = 0

    def draw_space_body(self, body):
        pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

    def run(self):
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)
            for body in self.bodies:
                self.draw_space_body(body)
            
            # Rotate planets
            self.rotate_space_body(self.mercury, self.sun)
            self.rotate_space_body(self.venus, self.sun)
            self.rotate_space_body(self.earth, self.sun)
            self.rotate_space_body(self.mars, self.sun)
            self.rotate_space_body(self.jupiter, self.sun)
            self.rotate_space_body(self.saturn, self.sun)
            self.rotate_space_body(self.uranus, self.sun)
            self.rotate_space_body(self.neptune, self.sun)
            self.rotate_space_body(self.pluto, self.sun)
            
            # Rotate Lua around Earth
            self.rotate_space_body(self.lua, self.earth)
            
            self.angle += 0.5
            
            pygame.display.flip()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def rotate_space_body(self, body, center_body):
        orbit_radius = ((center_body.x - body.x) ** 2 + (center_body.y - body.y) ** 2) ** 0.5
        body.x = center_body.x + orbit_radius * cos(radians(self.angle))
        body.y = center_body.y + orbit_radius * sin(radians(self.angle))

if __name__ == "__main__":
    app = SpaceApp()
    app.run()
    pygame.quit()