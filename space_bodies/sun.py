from core.space_body import SpaceBody

class Sun(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=50,
            skyfield_name='sun', 
            data_url='de421.bsp',
            name="Sun",
            color = "yellow",
            description="The sun is the center of the solar system and is a dynamic yellow dwarf star, constantly changing and sending energy out into space. It is a hot ball of plasma, inflated and heated by nuclear fusion reactions at its core. Internal energy is emitted as light, ultraviolet, and infrared radiation.",
            mass="1.99E+30 kg",
            diameter="1,400,000 km",
            AU="1 AU",
            avg_temperature="1.57E+07 °C",
            day="27 Earth days",
            year="2.30E+8 Earth years",
            category="Misc",
            texture_path="textures/misc/sun_texture.png",
            mu=132712440018,
            orbital_center_mu=0,
            semimajoraxis=0
        )
