from core.space_body import SpaceBody

class Lua(SpaceBody):
    def __init__(self, x, y):
        super().__init__(name="Lua", x=x, y=y, radius=4, color="lightgray", rotation_period=0.0748)  # About 27.3 days in Earth days
