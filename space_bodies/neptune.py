from core.space_body import SpaceBody

class Neptune(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=3.54, 
            color=(0.05, 0.21, 0.57),
            skyfield_name='neptune barycenter', 
            data_url='de421.bsp',
        )
