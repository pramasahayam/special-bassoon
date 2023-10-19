from core.space_body import SpaceBody

class Ariel(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='ariel', 
            data_url='de421.bsp',
            name="Ariel",
            description="Ariel is one of Uranus' moons and it is thought to consist of roughly equal amounts of water ice and silicate rock. It was discovered in 1851 by William Lassell who used his fortunes made in a brewery business to finance his telescopes.",
            mass="1.29E+21 kg",
            diameter="1,157.8 km",
            gravity="0.258 m/s²",
            orbit_distance="190,900 km"
        )
