from core.space_body import SpaceBody

class Io(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='io', 
            data_url='de421.bsp',
            name="Io",
            description="Io is Jupiter's moon and is the most volcanically active world in the solar system. It has hundreds of volcanoes with some erupting with lava dozens of miles high. Io is said to be caught in a tug-of-war between Jupiter's massive gravity and the smaller pull of Europa and Ganymede.",
            mass="8.93E+22 kg",
            diameter="3,643.2 km",
            gravity="1.796 m/s²",
            orbit_distance="421,800 km"
        )
