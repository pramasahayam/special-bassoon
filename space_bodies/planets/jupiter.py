from core.space_body import SpaceBody

class Jupiter(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=10.05, 
            skyfield_name='jupiter barycenter', 
            data_url='ephemeris_data/de421.bsp',
            name="Jupiter",
            description="Jupiter is the fifth planet from the Sun and is more than twice the size of any other planet in our solar system combined. The planet has a Great Red Spot that is a centuries-old storm bigger than the Earth. Jupiter is just a ball of hydrogen and helium.",
            mass="1.90E+27 kg",
            diameter="142,984 km",
            gravity="23.1 m/s^2",
            avg_temperature="-110 °C",
            day="0.414 Earth Days",
            year="11.86 Earth Years",
            category="Planets",
            texture_path="textures/planets/jupiter_texture.png"
        )
