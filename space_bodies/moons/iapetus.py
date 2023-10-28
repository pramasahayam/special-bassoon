from core.space_body import SpaceBody

class Iapetus(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.106,
            skyfield_name='iapetus', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat441.bsp',
            name="Iapetus",
            description="Iapetus is one of Saturn's moons and is called the yin yang of the Saturn moons because of its leading hemisphere reflectivity and its bright trailing hemisphere. It is Saturn's third-largest moon and was discovered in 1671 by Cassini.",
            mass="1.81E+21 kg",
            diameter="1,471.2 km",
            gravity="0.223 m/s²",
            orbit_distance="3,560,851 km",
            orbital_center=orbital_center
        )
