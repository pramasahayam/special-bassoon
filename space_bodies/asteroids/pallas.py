from core.space_body import SpaceBody

class Pallas(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5,
            skyfield_name='pallas', 
            data_url='de421.bsp',
            name="Pallas",
            color = "white",
            description="Pallas is the second asteroid to be discovered after Ceres. It is believed to have a mineral composition similar to carbonaceous chondrite meteorites. It is the third-largest asteroid in the solar system and it is most likely a remnant protoplanet.",
            mass="2.11E+20 kg",
            diameter="545 km",
            AU="3.392 AU",
            avg_temperature="-109.15 °C",
            day="0.325 Earth days",
            year="4.6 Earth years"
        )