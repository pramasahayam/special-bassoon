from core.space_body import SpaceBody

class Saturn(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=8.36, 
            color=(0.93, 0.89, 0.67),
            skyfield_name='saturn barycenter', 
            data_url='de421.bsp',
            mu=37931206.23,
            orbital_center_mu=132712440018,
            semimajoraxis=1426984171.8948
        )
