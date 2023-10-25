from core.space_body import SpaceBody

class Proteus(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='proteus', 
            data_url='de421.bsp',
            name="Proteus",
            description="Proteus is one of the largest known of Neptune's moons and has an odd box-like shape. It was discovered in 1989 by the Voyager 2. It is heavily cratered but shows no sign of geological modification. It is one of the darkest objects in our solar system and remains close to Neptune's equatorial plane.",
            mass="5.04E+19 kg",
            diameter="420 km",
            gravity="0.76 m/s²",
            orbit_distance="117,6460 km"
        )
