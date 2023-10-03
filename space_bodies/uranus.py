from core.space_body import SpaceBody

class Uranus(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Uranus", x=x, y=y, radius=25, color="lightseagreen", rotation_period=84.01)  # 84.01 Earth years
