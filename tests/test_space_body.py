import unittest
from core.space_body import SpaceBody

class TestSpaceBody(unittest.TestCase):
    def setUp(self):
        self.earth = SpaceBody(name="Earth", x=0, y=0, radius=16, color="blue", rotation_period=1.0)

    def test_initialization(self):
        self.assertEqual(self.earth.name, "Earth")
        self.assertEqual(self.earth.x, 0)
        self.assertEqual(self.earth.y, 0)
        self.assertEqual(self.earth.radius, 16)
        self.assertEqual(self.earth.color, "blue")
        self.assertEqual(self.earth.rotation_period, 1.0)

    # Add more tests as needed

if __name__ == "__main__":
    unittest.main()