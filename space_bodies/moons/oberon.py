from core.space_body import SpaceBody

class Oberon(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.109,
            skyfield_name='oberon', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/ura111l.bsp',
            name="Oberon",
            description="Oberon is the second-largest moon of Uranus and was discovered in 1787. Little was known about it until Voyager 2 passed it in 1986. The surface is heavily cratered and it is composed of roughly half ice and half rock. It has at least one large mountain that is 6 km tall.",
            mass="2.88E+21 kg",
            diameter="1,522.8 km",
            gravity="0.332 m/s²",
            orbit_distance="583,500 km",
            orbital_center=orbital_center,
            category="Moon",
            texture_path="textures/moons/moon_texture1.png"
        )
