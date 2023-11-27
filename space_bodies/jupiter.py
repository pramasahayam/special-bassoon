from core.space_body import SpaceBody

class Jupiter(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=10.04, 
            color=(0.93, 0.57, 0.13),
            skyfield_name='jupiter barycenter', 
            data_url='de421.bsp',
            mu=126686531.9,
            orbital_center_mu=132712440018,
            semimajoraxis=778327803.2388
        )
