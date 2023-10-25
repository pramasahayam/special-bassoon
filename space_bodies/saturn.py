from core.space_body import SpaceBody

class Saturn(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=8.38, 
            color=(0.93, 0.89, 0.67),
            skyfield_name='saturn barycenter', 
            data_url='de421.bsp',
        )
