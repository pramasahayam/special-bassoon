from core.space_body import SpaceBody

class Sun(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Sun", x=x, y=y, radius=50, color="yellow", rotation_period=None)