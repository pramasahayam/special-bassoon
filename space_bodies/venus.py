from core.space_body import SpaceBody

class Venus(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.87, 
            color=(0.91, 0.76, 0.65),
            skyfield_name='venus barycenter', 
            data_url='de421.bsp',
        )
