from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.92,
            color=(0, 0.5, 1),
            skyfield_name='earth barycenter',
            data_url='de421.bsp',
            orbital_center=None,
            name="Earth",
            description="Third planet from the Sun and the only known planet to harbor life."
        )
