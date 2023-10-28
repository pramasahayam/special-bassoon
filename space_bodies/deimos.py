from core.space_body import SpaceBody

class Deimos(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 0.25,
            color=(0.8, 0.8, 0.8),
            skyfield_name='deimos', 
            data_url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/mar097.bsp',
            name="Deimos",
            description="Deimos is Mars' moon and spings around Mars every 30 hours. It is the smaller of Mars' two moons and was discovered in 1877. It is composed of C-type rock, similar to blackish carbonaceous chondrite asteroids.",
            mass="1.48E+15 kg",
            diameter="12.4 km",
            gravity="0.003 m/s²",
            orbit_distance="23,458 km"
        )
