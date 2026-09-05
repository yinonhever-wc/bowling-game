import unittest
from bowling_game import BowlingGame, GameEndedError, InvalidPinsError, InvalidPinsTotalInFrameError

class TestBowlingGame(unittest.TestCase):
    """Test suite for bowling_game module."""

    def tearDown(self):
        """Runs after every test method."""
        pass
        
    def test_game_ended(self):
        game = BowlingGame()
        for _ in range(20):
            game.roll(3)
        with self.assertRaises(GameEndedError):
            game.roll(3)
            
    def test_negative_pins(self):
        game = BowlingGame()
        with self.assertRaises(InvalidPinsError):
            game.roll(-1)
            
    def test_pins_over_10(self):
        game = BowlingGame()
        with self.assertRaises(InvalidPinsError):
            game.roll(11)
            
    def test_invalid_total_in_regular_frame(self):
        game = BowlingGame()
        game.roll(7)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(4)
            
    def test_invalid_total_in_last_frame_with_strike(self):
        game = BowlingGame()
        for _ in range(18):
            game.roll(3)
        game.roll(10)
        game.roll(7)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(4)
            
    def test_invalid_total_in_last_frame_without_strike(self):
        game = BowlingGame()
        for _ in range(18):
            game.roll(3)
        game.roll(8)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(7)
            
    def test_strike_with_full_next_frame(self):
        game = BowlingGame()
        game.roll(10)
        game.roll(6)
        game.roll(2)
        self.assertEqual(game.score(), 26)
    
    def test_strike_with_partial_next_frame(self):
        game = BowlingGame()
        game.roll(10)
        game.roll(6)
        self.assertEqual(game.score(), 22)
        
    def test_strike_without_next_frame(self):
        game = BowlingGame()
        game.roll(10)
        self.assertEqual(game.score(), 10)
    
    def test_unfinished_game_with_spare(self):
        game = BowlingGame()
        game.roll(7)
        game.roll(3)
        game.roll(4)
        game.roll(2)
        self.assertEqual(game.score(), 20)
        
    def test_unfinished_regular_game(self):
        game = BowlingGame()
        game.roll(6)
        game.roll(3)
        game.roll(4)
        game.roll(2)
        self.assertEqual(game.score(), 15)

if __name__ == "__main__":
    unittest.main()