from core.space_body import SpaceBody

class Mars(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=9.8, # Multiplied by 20 for testing
            color=(0.8, 0.49, 0.19),
            skyfield_name='mars barycenter', 
            data_url='de421.bsp',
            name="Mars"
            mu=42828.37362
            orbital_center_mu=132712440018
            semimajoraxis=228480828.3783
        )
