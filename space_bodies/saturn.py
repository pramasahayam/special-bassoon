from core.space_body import SpaceBody

class Saturn(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Saturn", x=x, y=y, radius=30, color="gold", rotation_period=29.46)  # 29.46 Earth years
