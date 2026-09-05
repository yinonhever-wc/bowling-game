import unittest
from example_usage import example_game, perfect_game, all_spares, gutter_game, regular_game

class TestExampleUsage(unittest.TestCase):
    """
    Test suite for example_usage module.
    This suite tests the 5 examples of full games included in that module, checking if each game
    receives the correct final score based on its rolls.
    """

    def tearDown(self):
        """Runs after every test method."""
        pass

    def test_example_game(self):
        """Testing an example game where occasional strikes and spares are combined with regular scores.
        This specific game scenario should result in a total score of 190."""
        result = example_game()
        self.assertEqual(result, 190)

    def test_perfect_game(self):
        """Testing a perfect game scenario where all rolls achieve a strike (10 pins). 
        It should result in a total score of 300."""
        result = perfect_game()
        self.assertEqual(result, 300)
        
    def test_all_spares(self):
        """Testing a game scenario where a spare was achieved in each frame (5 pins in each roll),
        followed by 5 pins in the extra roll of the last frame.
        It should result in a total score of 150."""
        result = all_spares()
        self.assertEqual(result, 150)
        
    def test_gutter_game(self):
        """Testing a game scenario where no pins were scored in any rolls throughout the entire game.
        It should result in a total score of 0."""
        result = gutter_game()
        self.assertEqual(result, 0)

    def test_regular_game(self):
        """Testing a game scenario without any strikes or spares throughout the entire game.
        This specific scenario should result in a total score of 72."""
        result = regular_game()
        self.assertEqual(result, 72)

if __name__ == "__main__":
    unittest.main()