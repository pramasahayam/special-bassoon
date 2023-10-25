from core.space_body import SpaceBody

class Nereid(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='nereid', 
            data_url='de421.bsp',
            name="Nereid",
            description="Nereid is the outermost of Neptune's moons and is among the largest. It was discovered in 1949 with a ground-based telescope and it was the last satellite of Neptune to be discovered before Voyager 2. It has one of the most eccentric orbits of any moon in the solar system.",
            mass="3.09E+19 kg",
            diameter="340 km",
            gravity="0.071 m/s²",
            orbit_distance="5,513,818 km"
        )
