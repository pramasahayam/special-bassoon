from core.space_body import SpaceBody

class Jupiter(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=10.05, 
            color=(0.93, 0.57, 0.13),
            skyfield_name='jupiter barycenter', 
            data_url='de421.bsp',
        )
