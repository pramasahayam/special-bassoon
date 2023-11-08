from core.space_body import SpaceBody

class Europa(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.224,
            skyfield_name='europa', 
            data_url='jup365.bsp',
            name="Europa",
            description="Europa is one of Jupiter's moons and is the sixth closest moon to the planet. It is one of its largest and most well-known moons. Europa was discovered in 1610 when Galileo Galilei viewed it with his homemade telescope. It is primarily made of silicate rock, a water-ice crust, and a nickel core",
            mass="4.80E+22 kg",
            diameter="3,121.6 km",
            gravity="1.315 m/s²",
            orbit_distance="671,100 km",
            orbital_center=orbital_center,
            category="Moons",
            texture_path="textures/moons/moon_texture1.png"
        )
