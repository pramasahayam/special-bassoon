import tkinter as tk
from math import cos, sin, radians

from space_bodies import Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

class SpaceApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, bg="black", width=1600, height=1200)
        self.canvas.pack(padx=10, pady=10)

        # Initialize Sun and all planets
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

        # Create visual representations on the canvas
        self.sun_id = self.create_space_body(self.sun)
        self.mercury_id = self.create_space_body(self.mercury)
        self.venus_id = self.create_space_body(self.venus)
        self.earth_id = self.create_space_body(self.earth)
        self.mars_id = self.create_space_body(self.mars)
        self.jupiter_id = self.create_space_body(self.jupiter)
        self.saturn_id = self.create_space_body(self.saturn)
        self.uranus_id = self.create_space_body(self.uranus)
        self.neptune_id = self.create_space_body(self.neptune)
        self.pluto_id = self.create_space_body(self.pluto)

        # Rotate planets around the sun
        self.rotate_space_body(self.mercury, self.mercury_id)
        self.rotate_space_body(self.venus, self.venus_id)
        self.rotate_space_body(self.earth, self.earth_id)
        self.rotate_space_body(self.mars, self.mars_id)
        self.rotate_space_body(self.jupiter, self.jupiter_id)
        self.rotate_space_body(self.saturn, self.saturn_id)
        self.rotate_space_body(self.uranus, self.uranus_id)
        self.rotate_space_body(self.neptune, self.neptune_id)
        self.rotate_space_body(self.pluto, self.pluto_id)

    def create_space_body(self, body):
        return self.canvas.create_oval(
            body.x - body.radius, body.y - body.radius,
            body.x + body.radius, body.y + body.radius,
            fill=body.color
        )

    def rotate_space_body(self, body, body_id):
        angle = 0
        orbit_radius = ((self.sun.x - body.x)**2 + (self.sun.y - body.y)**2)**0.5  # Distance formula

        def update_position():
            nonlocal angle
            body.x = self.sun.x + orbit_radius * cos(radians(angle))
            body.y = self.sun.y + orbit_radius * sin(radians(angle))
            self.canvas.coords(
                body_id,
                body.x - body.radius, body.y - body.radius,
                body.x + body.radius, body.y + body.radius
            )

            angle_increment = 360 / (body.rotation_period * 365.25) * 5  # in degrees
            angle += angle_increment
            root.after(10, update_position)

        update_position()

root = tk.Tk()
root.title("Solar System Simulation")
app = SpaceApp(root)
root.mainloop()