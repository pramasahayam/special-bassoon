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
            mu=398600.436,
            orbital_center_mu=132712440018,
            semimajoraxis=149597871
        )
