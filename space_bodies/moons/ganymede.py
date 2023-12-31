from core.space_body import SpaceBody

class Ganymede(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.378,
            skyfield_name='ganymede', 
            data_url='jup365.bsp',
            name="Ganymede",
            color = "white",
            description="Ganymede is Jupiter's largest moon, the largest moon in our solar system, and even larger than Mercury and Pluto. There is evidence of an underground saltwater ocean that may hold more water than all of Earth's surface. It is the only moon known to have its own magnetic field.",
            mass="1.48E+23 kg",
            diameter="5,262.4 km",
            gravity="1.428 m/s²",
            orbit_distance="1,070,400 km",
            orbital_center=orbital_center,
            category="Moons",
            texture_path="textures/moons/moon_texture1.png",
            mu=9887.83275,
            orbital_center_mu=126686531.9,
            semimajoraxis=1070400
        )
