from core.space_body import SpaceBody

class Mercury(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Mercury", x=x, y=y, radius=10, color="gray", rotation_period=0.24)  # 0.24 Earth years
