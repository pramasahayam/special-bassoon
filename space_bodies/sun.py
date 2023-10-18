from core.space_body import SpaceBody

class Sun(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=100,
            color=(1, 1, 0),
            skyfield_name='sun', 
            data_url='de421.bsp',  # The specific URL or file path for the sun's data
            name="Sun",
            description="The sun is the center of the solar system and is a dynamic yellow dwarf star, constantly changing and sending energy out into space. It is a hot ball of plasma, inflated and heated by nuclear fusion reactions at its core. Internal energy is emitted as light, ultraviolet, and infrared radiation.",
            mass="1.99E+30 kg",
            diameter="1,400,000 km",
            AU="1 AU",
            gravity="274.0 m/s²",
            avg_temperature="1.57E+07 °C",
        )
