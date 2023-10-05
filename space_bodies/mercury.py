from core.space_body import SpaceBody

class Mercury(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.35, 
            color=(0.83, 0.68, 0.21),  # Arbitrary color for visualization
            skyfield_name='mercury barycenter', 
            data_url='de421.bsp',
        )