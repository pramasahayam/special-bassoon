from core.space_body import SpaceBody

class Pluto(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=100.74, 
            color=(0.66, 0.44, 0.09),
            skyfield_name='pluto barycenter', 
            data_url='de421.bsp',
        )
