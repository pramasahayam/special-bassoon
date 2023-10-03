from core.space_body import SpaceBody

class Pluto(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Pluto", x=x, y=y, radius=8, color="chocolate", rotation_period=248.6)  # 248.6 Earth years
