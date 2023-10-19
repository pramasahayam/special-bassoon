from core.space_body import SpaceBody

class Sedna(SpaceBody):
    def __init__(self):
        super().__init__(
            radius= 5, # Multiplied by 20 for testing
            color=(0.8, 0.8, 0.8),
            skyfield_name='sedna', 
            data_url='de421.bsp',
            name="Sedna",
            description="Sedna is a dwarf planet in the outmost reaches of the solar system. It was discovered in 2003 and its surface is composed of a mix of water, methane, and nitrogen ice. It is one of the reddest solar system objects.",
            mass="1.70E+22 kg",
            diameter="995 km",
            gravity="0.33 m/s²",
            avg_temperature="-261.15 °C",
            day="0.417 Earth days",
            year="11,408 Earth years"
        )