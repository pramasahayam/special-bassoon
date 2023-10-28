from core.space_body import SpaceBody

class Phobos(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= .17,
            skyfield_name='phobos', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/mar097.bsp',
            name="Phobos",
            description="Phobos is Mars' moon and orbits Mars three times a day. It has many grooves and craters from thousands of meteorite impacts. It is composed of C-type rock, similar to blackish carbonaceous chondrite asteroids.",
            mass="1.07E+16 kg",
            diameter="22.2 km",
            gravity="0.0057 m/s²",
            orbit_distance="9,376 km",
            orbital_center=orbital_center
        )
