from core.space_body import SpaceBody

class Rhea(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='rhea', 
            data_url='de421.bsp',
            name="Rhea",
            description="Rhea is the second largest of Saturn's moons but is less than a third of the radius of Saturn's largest moon, Titan. It is a small, cold, airless body and is tidally locked in phase with Saturn, always with one side facing toward it. It is highly reflective, suggesting a surface of water ice.",
            mass="2.31E+21 kg",
            diameter="1,528.6 km",
            gravity="0.264 m/s²",
            orbit_distance="527,068 km"
        )
