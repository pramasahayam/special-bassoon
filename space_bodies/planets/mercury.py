from core.space_body import SpaceBody

class Mercury(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.35, 
            skyfield_name='mercury barycenter', 
            data_url='de421.bsp',
            name="Mercury",
            description="Mercury is the smallest planet in our solar system and the closest to the sun. It zips around the sun every 88 Earth days. From the surface of Mercury, the Sun would appear more than 3x larger than when viewed on Earth.",
            mass="3.30E+23 kg",
            diameter="4,878 km",
            gravity="3.7 m/s^2",
            avg_temperature="167 °C",
            day="59 Earth Days",
            year="0.241 Earth Years",
            category="Planets",
            texture_path="textures/planets/mercury_texture.png",
            mu=22032,
            orbital_center_mu=132712440018,
            semimajoraxis=57909336
        )