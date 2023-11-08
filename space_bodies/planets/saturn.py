from core.space_body import SpaceBody

class Saturn(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=8.38, 
            skyfield_name='saturn barycenter', 
            data_url='de421.bsp',
            name="Saturn",
            description="Saturn is the sixth planet from the Sun and is the second largest planet in our solar system. Saturn has beautiful icy rings that are more spectacular and complicated than any other planet. Saturn is a ball of mostly hydrogen and helium.",
            mass="5.68E+26 kg",
            diameter="102,536 km",
            gravity="9 m/s^2",
            avg_temperature="-140 °C",
            day="0.446 Earth Days",
            year="29 Earth Years",
            category="Planets",
            texture_path="textures/planets/saturn_texture.png"
        )
