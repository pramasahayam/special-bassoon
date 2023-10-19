from core.space_body import SpaceBody

class Triton(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='triton', 
            data_url='de421.bsp',
            name="Triton",
            description="Triton is the largest of Neptune's moons and was discovered in 1846. It is unusual because it is the only large moon in our solar system that orbits in the opposite direction of its planet's rotation. It shares similarities with Pluto, which makes scientists believe it is a Kuiper Bely Object captured by Neptune's gravity.",
            mass="2.14E+22 kg",
            diameter="2,706.8 km",
            gravity="0.779 m/s²",
            orbit_distance="354,759 km"
        )
