from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=9.10,  # Multiplied by 10 for testing
            color=(0, 0.5, 1),
            skyfield_name='earth barycenter',
            data_url='de421.bsp',
            speed_multiplier=1.0,
            orbital_center=None,
            name="Earth",
            description="Third planet from the Sun and the only known planet to harbor life."
        )
