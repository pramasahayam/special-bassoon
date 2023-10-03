from core.space_body import SpaceBody

class Jupiter(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Jupiter", x=x, y=y, radius=35, color="orange", rotation_period=11.86)  # 11.86 Earth years
