from core.space_body import SpaceBody

class Mars(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.49,
            skyfield_name='mars barycenter', 
            data_url='de421.bsp',
            name="Mars",
            description="Mars is the fourth planet from the Sun and is a dusty, cold, desert-like world with a thin atmosphere. Mars is one of the most explored bodies and has a very dynamic landscape with polar ice caps, canyons, and extinct volcanoes.",
            mass="6.42E+23 kg",
            diameter="6,792 km",
            gravity="3.7 m/s^2",
            avg_temperature="-65 °C",
            day="1.025 Earth Days",
            year="1.881 Earth Years",
            texture_path="textures/planets/mars_texture.png"
        )
