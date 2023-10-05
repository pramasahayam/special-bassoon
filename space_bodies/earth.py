from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.91,  # This is a smaller value than Sun's radius to make it visible
            color=(0, 0.5, 1),
            skyfield_name='earth barycenter',
            data_url='de421.bsp',
            speed_multiplier=1.0,
            orbital_center=None
        )
