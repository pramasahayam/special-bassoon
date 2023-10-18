from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=18.2,  # Multiplied by 20 for testing
            color=(0, 0.5, 1),
            skyfield_name='earth barycenter',
            data_url='de421.bsp',
            orbital_center=None,
            name="Earth",
            description="Third planet from the Sun and the only known planet to harbor life.",
            mass="5.97E+24 kg",
            diameter="12,756 km",
            gravity="9.8 m/s^2",
            avg_temperature="15 °C",
            day="1 Earth Day",
            year="1 Earth Year",
        )
