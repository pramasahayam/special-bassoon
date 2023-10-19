from core.space_body import SpaceBody

class Hygiea(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='Hygiea', 
            data_url='de421.bsp',
            name="Hygiea",
            description="Hygiea is a major asteroid located in the asteroid belt. It is the fourth-largest asteroid in the solar system. It is the largest of the dark C-type asteroids with a carbonaceous surface. It was revealed in 2019 that Hygiea's shape is nearly spherical, which is why it can possibly become a new dwarf planet.",
            mass="8.67E+19 kg",
            diameter="430 km",
            AU="2.41 AU",
            avg_temperature="-115.15 °C",
            day="0.575 Earth days",
            year="5.56 Earth years"
        )
