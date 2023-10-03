from core.space_body import SpaceBody

class Neptune(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Neptune", x=x, y=y, radius=24, color="blue", rotation_period=164.8)  # 164.8 Earth years
