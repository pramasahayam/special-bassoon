from core.space_body import SpaceBody

class Moon(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 0.25,
            color=(0.8, 0.8, 0.8),
            skyfield_name='moon', 
            data_url='de421.bsp',
            name="Luna",
            description="The Moon is Earth's only natural satellite. It is one of the largest natural satellites in the Solar System, and the largest among planetary satellites relative to the size of the planet that it orbits. The Moon is the second-densest satellite, after Io, a satellite of Jupiter.",
            mass="7.30E+22 kg",
            diameter="3,474.8 km",
            gravity="1.6 m/s²",
            orbit_distance="384,400 km",
        )
