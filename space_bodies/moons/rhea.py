from core.space_body import SpaceBody

class Rhea(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.110,
            skyfield_name='rhea', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/sat441x1_part-1.bsp',
            name="Rhea",
            description="Rhea is the second largest of Saturn's moons but is less than a third of the radius of Saturn's largest moon, Titan. It is a small, cold, airless body and is tidally locked in phase with Saturn, always with one side facing toward it. It is highly reflective, suggesting a surface of water ice.",
            mass="2.31E+21 kg",
            diameter="1,528.6 km",
            gravity="0.264 m/s²",
            orbit_distance="527,068 km",
            orbital_center=orbital_center,
            category="Moons",
            texture_path="textures/moons/moon_texture1.png"
        )
