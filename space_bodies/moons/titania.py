from core.space_body import SpaceBody

class Titania(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 5,
            skyfield_name='titania', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/ura111l.bsp',
            name="Titania",
            description="Titania is Uranus' largest moon and 200 years after it was discovered, it was revealed that the moon is geologically active. It has a prominent system of fault valleys, some which are nearly 1,609 km long. Deposits of highly reflective material can be seen along the Sun-facing valley wall, which may represent frost.",
            mass="3.42E+21 kg",
            diameter="1,577.8 km",
            gravity="0.367 m/s²",
            orbit_distance="436,300 km",
            orbital_center=orbital_center
        )
