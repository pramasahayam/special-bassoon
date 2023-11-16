from core.space_body import SpaceBody

class Earth(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.92,
            skyfield_name='earth barycenter',
            data_url='de421.bsp',
            orbital_center=None,
            name="Earth",
            color = "teal",
            description="Third planet from the Sun and the only known planet to harbor life.",
            mass="5.97E+24 kg",
            diameter="12,756 km",
            gravity="9.8 m/s^2",
            avg_temperature="15 °C",
            day="1 Earth Day",
            year="1 Earth Year",
            category="Planets",
            texture_path="textures/planets/earth_texture.png"
        )
