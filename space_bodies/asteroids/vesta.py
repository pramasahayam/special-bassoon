from core.space_body import SpaceBody

class Vesta(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5,
            skyfield_name='vesta', 
            data_url='de421.bsp',
            name="Vesta",
            description="Vesta is the second largest body in the asteroid belt, only surpassed by Ceres. It is the brightest asteroid in the sky and is occasionally visible from Earth with the naked eye. It is the first of the four asteroid belt objects to be visited by a spacecraft, NASA's Dawn.",
            mass="2.67E+20 kg",
            diameter="530 km",
            AU="1.14 AU",
            avg_temperature="-110.5 °C",
            day="0.223 Earth days",
            year="3.63 Earth years"
        )