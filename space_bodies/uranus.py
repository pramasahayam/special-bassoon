from core.space_body import SpaceBody

class Uranus(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=3.64, 
            color=(0.56, 0.75, 0.78),
            skyfield_name='uranus barycenter', 
            data_url='de421.bsp',
            mu=5793951.3,
            orbital_center_mu=132712440018,
            semimajoraxis=2870992581.5094
        )
