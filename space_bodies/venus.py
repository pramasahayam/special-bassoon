from core.space_body import SpaceBody

class Venus(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Venus", x=x, y=y, radius=15, color="goldenrod", rotation_period=0.62)  # 0.62 Earth years
