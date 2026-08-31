import unittest
from example_usage import example_game, perfect_game, all_spares, gutter_game, regular_game

class TestExampleUsage(unittest.TestCase):
    """Test suite for example_usage module."""

    def tearDown(self):
        """Runs after every test method."""
        pass

    def test_example_game(self):
        result = example_game()
        self.assertEqual(result, 190)

    def test_perfect_game(self):
        result = perfect_game()
        self.assertEqual(result, 300)
        
    def test_all_spares(self):
        result = all_spares()
        self.assertEqual(result, 150)
        
    def test_gutter_game(self):
        result = gutter_game()
        self.assertEqual(result, 0)

    def test_regular_game(self):
        result = regular_game()
        self.assertEqual(result, 72)

if __name__ == "__main__":
    unittest.main()