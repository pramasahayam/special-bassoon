from core.space_body import SpaceBody

class Mars(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.49,
            skyfield_name='mars barycenter', 
            data_url='de421.bsp',
            name="Mars",
            color = "red",
            description="Mars is the fourth planet from the Sun and is a dusty, cold, desert-like world with a thin atmosphere. Mars is one of the most explored bodies and has a very dynamic landscape with polar ice caps, canyons, and extinct volcanoes.",
            mass="6.42E+23 kg",
            diameter="6,792 km",
            gravity="3.7 m/s^2",
            avg_temperature="-65 °C",
            day="1.025 Earth Days",
            year="1.881 Earth Years",
            category="Planets",
            texture_path="textures/planets/mars_texture.png",
            mu=42828.37362,
            orbital_center_mu=132712440018,
            semimajoraxis=228480828.3783
        )
