from core.space_body import SpaceBody

class Ceres(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5,
            skyfield_name='ceres', 
            data_url='de421.bsp',
            name="Ceres",
            color = "white",
            description="Ceres was once the largest asteroid but is now considered a dwarf planet since 2006 since it is so different from its neighbors. It is the largest object in the asteroid belt between Mars and Jupiter and it is the only dwarf planet located In the inner solar system. It is the first dwarf planet to be visited by a spacecraft, NASA's Dawn.",
            mass="9.10E+20 kg",
            diameter="952 km",
            gravity="0.27 m/s²",
            avg_temperature="-108 °C",
            day="0.375 Earth days",
            year="5 Earth years"
        )