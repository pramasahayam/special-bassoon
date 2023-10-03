from core.space_body import SpaceBody

class Mars(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Mars", x=x, y=y, radius=14, color="red", rotation_period=1.88)  # 1.88 Earth years
