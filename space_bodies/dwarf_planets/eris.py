from core.space_body import SpaceBody

class Eris(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5,
            skyfield_name='eris', 
            data_url='de421.bsp',
            name="Eris",
            description="Eris is one of the largest known dwarf planets in our solar system, being about the same size as Pluto but it is three times farther from the Sun. Eris was discovered in 2005. The surface is extremely cold and most likely has a surface similar to Pluto.",
            mass="1.67E+22 kg",
            diameter="2,324 km",
            gravity="0.82 m/s²",
            avg_temperature="-230 °C",
            day="1.08 Earth days",
            year="557 Earth years"
        )