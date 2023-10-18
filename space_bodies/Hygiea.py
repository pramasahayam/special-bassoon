from core.space_body import SpaceBody

class Hygiea(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='Hygiea', 
            data_url='de421.bsp',
            name="Hygiea",
            age="4.51 billion years",
            description="The Moon is Earth's only natural satellite. It is one of the largest natural satellites in the Solar System, and the largest among planetary satellites relative to the size of the planet that it orbits. The Moon is the second-densest satellite, after Io, a satellite of Jupiter.",
            mass="7.30E+22 kg",
            diameter="3,474.8 km",
            gravity="1.6 m/s²",
            avg_temperature="-23 °C",
            orbit_distance="384,400 km"
        )