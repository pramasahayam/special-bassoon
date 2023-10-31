from core.space_body import SpaceBody

class Uranus(SpaceBody):
    def __init__(self):
        super().__init__(
            radius=3.64, 
            skyfield_name='uranus barycenter', 
            data_url='de421.bsp',
            name="Uranus",
            description="Uranus is the seventh planet from the Sun and rotates at nearly a 90-degree angle from the plane of its orbit. This makes it appear that it is spinning on its side. Uranus is considered an ice giant as its mass is mostly made of water, methane, and ammonia.",
            mass="8.68E+25 kg",
            diameter="51,118 km",
            gravity="8.7 m/s^2",
            avg_temperature="-195 °C",
            day="0.719 Earth Days",
            year="84 Earth Years"
        )
