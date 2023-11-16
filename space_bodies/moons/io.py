from core.space_body import SpaceBody

class Io(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.262,
            skyfield_name='io', 
            data_url='jup365.bsp',
            name="Io",
            color = "white",
            description="Io is Jupiter's moon and is the most volcanically active world in the solar system. It has hundreds of volcanoes with some erupting with lava dozens of miles high. Io is said to be caught in a tug-of-war between Jupiter's massive gravity and the smaller pull of Europa and Ganymede.",
            mass="8.93E+22 kg",
            diameter="3,643.2 km",
            gravity="1.796 m/s²",
            orbit_distance="421,800 km",
            orbital_center=orbital_center,
            category="Moons",
            texture_path="textures/moons/moon_texture1.png"
        )
