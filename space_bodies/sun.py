from core.space_body import SpaceBody

class Sun(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=100, 
            color=(1, 1, 0), 
            skyfield_name='sun', 
            data_url='de421.bsp',  # The specific URL or file path for the sun's data
            speed_multiplier=1.0,
            name="Sun",
            description="PRAISE THE SUN"
        )
