from core.space_body import SpaceBody

class Venus(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=0.87, 
            skyfield_name='venus barycenter', 
            data_url='de421.bsp',
            name="Venus",
            description="Venus is the second planet from the Sun and is the hottest planet in our solar system. It spins slowly in the opposite direction from most planets and has a thick atmosphere that traps heat.",
            mass="4.87E+24 kg",
            diameter="12,104 km",
            gravity="8.9 m/s^2",
            avg_temperature="464 °C",
            day="243 Earth Days",
            year="0.616 Earth Years",
            category="Planet",
            texture_path="textures/planets/venus_texture.png"
        )
