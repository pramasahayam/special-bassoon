from core.space_body import SpaceBody

class Titan(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.370,
            skyfield_name='titan', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat441.bsp',
            name="Titan",
            description="Titan is Saturn's largest moon and it is the only moon in our solar system with a substantial atmosphere. It is the only place besides Earth known to have liquids in the form of rivers, lakes, and seas on its surface. Titan is also larger than Mercury and the second-largest moon in our solar system.",
            mass="1.35E+23 kg",
            diameter="5,149.4 km",
            gravity="1.354 m/s²",
            orbit_distance="1,221,865 km",
            orbital_center=orbital_center,
            category="Moon",
            texture_path="textures/moons/moon_texture1.png"
        )
