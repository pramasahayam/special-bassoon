from core.space_body import SpaceBody

class Callisto(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.346,
            skyfield_name='callisto', 
            data_url='jup365.bsp',
            name="Callisto",
            color = "white",
            description="Callisto is Jupiter's second-largest moon and the third-largest in our solar system. It has multiple rings and is the most heavily cratered object in our solar system. It was discovered in 1610 and has a very icy surface that may be hiding a subsurface ocean.",
            mass="1.08E+23 kg",
            diameter="4,820.6 km",
            gravity="1.236 m/s²",
            orbit_distance="1,882,700 km",
            orbital_center=orbital_center,
            category="Moons",
            texture_path="textures/moons/moon_texture1.png"
        )
