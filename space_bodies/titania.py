from core.space_body import SpaceBody

class Titania(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='titania', 
            data_url='de421.bsp',
            name="Titania",
            description="Titania is Uranus' largest moon and 200 years after it was discovered, it was revealed that the moon is geologically active. It has a prominent system of fault valleys, some which are nearly 1,609 km long. Deposits of highly reflective material can be seen along the Sun-facing valley wall, which may represent frost.",
            mass="3.42E+21 kg",
            diameter="1,577.8 km",
            gravity="0.367 m/s²",
            orbit_distance="436,300 km"
        )
