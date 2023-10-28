from core.space_body import SpaceBody

class Neptune(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=3.54, 
            color=(0.05, 0.21, 0.57),
            skyfield_name='neptune barycenter', 
            data_url='de421.bsp',
            name="Neptune",
            description="Neptune is the eighth planet from the Sun and is the most distance major planet. It is dark, cold, and whipped with supersonic winds. Neptune was the first planet located through mathematical calculations.",
            mass="1.02E+26 kg",
            diameter="49,528 km",
            gravity="11 m/s^2",
            avg_temperature="-200 °C",
            day="0.667 Earth Days",
            year="165 Earth Years",
        )
