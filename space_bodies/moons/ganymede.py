from core.space_body import SpaceBody

class Ganymede(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.378,
            skyfield_name='ganymede', 
            data_url='jup365.bsp',
            name="Ganymede",
            description="Ganymede is Jupiter's largest moon, the largest moon in our solar system, and even larger than Mercury and Pluto. There is evidence of an underground saltwater ocean that may hold more water than all of Earth's surface. It is the only moon known to have its own magnetic field.",
            mass="1.48E+23 kg",
            diameter="5,262.4 km",
            gravity="1.428 m/s²",
            orbit_distance="1,070,400 km",
            orbital_center=orbital_center
        )
