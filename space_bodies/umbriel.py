from core.space_body import SpaceBody

class Umbriel(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='umbriel', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/ura111l.bsp',
            name="Umbriel",
            description="Umbriel is the darkest of Uranus' largest moons as it only reflects 16% of light that strikes the surface. Voyager 2 revealed a bright ring about 140 km in diameter and it is unclear what created the distinctive ring. It may be front deposits associated with an impact crater.",
            mass="1.22E+21 kg",
            diameter="1,169.4 km",
            gravity="0.238 m/s²",
            orbit_distance="266,000 km"
        )
