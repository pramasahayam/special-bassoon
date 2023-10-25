from core.space_body import SpaceBody

class Pluto(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.27, 
            color=(0.66, 0.44, 0.09),
            skyfield_name='pluto barycenter', 
            data_url='de421.bsp',
            name="Pluto",
            description="Pluto was once considered the ninth planet from the Sun but is now the best-known dwarf planet. It is a world of ice mountains and frozen planes. Pluto is located in the Kuiper Belt, a donut-shaped region beyond the orbit of Neptune.",
            mass="1.31E+22 kg",
            diameter="2,302 km",
            gravity="0.66 m/s^2",
            avg_temperature="-232 °C",
            day="27 Earth Days",
            year="2.30E+08 Earth Years",
        )
