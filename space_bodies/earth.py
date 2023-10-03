from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Earth", x=x, y=y, radius=16, color="blue", rotation_period=1.0)  # 1 Earth year
