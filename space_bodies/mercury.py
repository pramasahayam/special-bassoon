from core.space_body import SpaceBody

class Mercury(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.35, 
            color=(0.83, 0.68, 0.21),  # Arbitrary color for visualization
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
            texture_path="textures/planets/mercury_texture.png"
        )