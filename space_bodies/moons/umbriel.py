from core.space_body import SpaceBody

class Umbriel(SpaceBody):
    def __init__(self, orbital_center=None):
        super().__init__(
            radius= 0.084,
            skyfield_name='umbriel', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/ura111l.bsp',
            name="Umbriel",
            description="Umbriel is the darkest of Uranus' largest moons as it only reflects 16% of light that strikes the surface. Voyager 2 revealed a bright ring about 140 km in diameter and it is unclear what created the distinctive ring. It may be front deposits associated with an impact crater.",
            mass="1.22E+21 kg",
            diameter="1,169.4 km",
            gravity="0.238 m/s²",
            orbit_distance="266,000 km",
            orbital_center=orbital_center,
            scaling_multiplier=50,
            distance_multiplier=1.25
        )
