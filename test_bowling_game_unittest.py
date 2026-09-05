import unittest
from bowling_game import BowlingGame, GameEndedError, InvalidPinsError, InvalidPinsTotalInFrameError

class TestBowlingGame(unittest.TestCase):
    """
    Test suite for bowling_game module.
    This suit tests edge cases and invalid game scenarios that should result in an error,
    as well as scenarios of partial or unfinished valid games.
    """

    def tearDown(self):
        """Runs after every test method."""
        pass
        
    def test_game_ended(self):
        """Testing an invalid scenario of attempting to roll again after all 10 frames have been played put and the game 
        has already ended. 
        In this case the number 3 is rolled 20 times, which ends the game, and then and the number 3 is rolled again, which 
        should result in a GameEndedError being raised."""
        game = BowlingGame()
        for _ in range(20):
            game.roll(3)
        with self.assertRaises(GameEndedError):
            game.roll(3)
            
    def test_negative_pins(self):
        """Testing an invalid scenario of attempting to roll a negative number of pins.
        In this case the code attempts to roll -1 pins, outside the valid range of 0-10.
        It should result in an InvalidPinsError being raised."""
        game = BowlingGame()
        with self.assertRaises(InvalidPinsError):
            game.roll(-1)
            
    def test_pins_over_10(self):
        """Testing an invalid scenario of attempting to roll a number of pins higher than 10.
        In this case the code attempts to roll 11 pins, outside the valid range of 0-10.
        It should result in an InvalidPinsError being raised."""
        game = BowlingGame()
        with self.assertRaises(InvalidPinsError):
            game.roll(11)
            
    def test_invalid_total_in_regular_frame(self):
        """Testing an invalid scenario of attempting to roll a total number of pins higher than 10 in a regular frame
        (one of the first 9 frames, where a maximum of 2 rolls is possible).
        In this case the numbers 7 and 4 are rolled in the first frame, for an invalid total of 11 pins.
        It should result in an InvalidPinsTotalInFrameError being raised."""
        game = BowlingGame()
        game.roll(7)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(4)
            
    def test_invalid_total_in_last_frame_with_strike(self):
        """Testing an invalid scenario of attempting to roll a total number of pins higher than 10 in the last two rolls
        of the 10th frame, after a strike in the frame's first roll, but without a strike in the second roll.
        In this case, after rolling 10 on the frame's 1st roll, the numbers 7 and 4 are rolled in the 2nd and 3rd rolls 
        respectively, for an invalid total of 11 pins in these two rolls (the maximum total allowed for these two rolls is 10,
        since the 2nd roll isn't a strike).
        It should result in an InvalidPinsTotalInFrameError being raised."""
        game = BowlingGame()
        for _ in range(18):
            game.roll(3)
        game.roll(10)
        game.roll(7)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(4)
            
    def test_invalid_total_in_last_frame_without_strike(self):
        """Testing an invalid scenario of attempting to roll a total number of pins higher than 10 in the first two rolls
        of the 10th frame, without a strike occuring in that frame.
        In this case, the numbers 7 and 4 are rolled in the frame, for an invalid total of 11 - the maximum total allowed 
        for these two rolls is 10, since no strike was achieved in the frame's first roll.
        It should result in an InvalidPinsTotalInFrameError being raised."""
        game = BowlingGame()
        for _ in range(18):
            game.roll(3)
        game.roll(8)
        with self.assertRaises(InvalidPinsTotalInFrameError):
            game.roll(7)
            
    def test_strike_with_full_next_frame(self):
        """Testing an unfinished valid game scenario where a strike happens in the first frame, and a full frame is
        played afterwards.
        
        Frames and scoring:
        Frame 1: 10
        Frame 2: 6, 2
        
        Total expected score: 26
        """
        game = BowlingGame()
        game.roll(10)
        game.roll(6)
        game.roll(2)
        self.assertEqual(game.score(), 26)
    
    def test_strike_with_partial_next_frame(self):
        """Testing an unfinished valid game scenario where a strike happens in the first frame, and a partial frame is
        played afterwards.
        
        Frames and scoring:
        Frame 1: 10
        Frame 2: 6
        
        Total expected score: 22
        """
        game = BowlingGame()
        game.roll(10)
        game.roll(6)
        self.assertEqual(game.score(), 22)
        
    def test_strike_without_next_frame(self):
        """Testing an unfinished valid game scenario where a strike happens in the first frame, 
        and no rolls are done afterwards.
        
        Frames and scoring:
        Frame 1: 10
        
        Total expected score: 10
        """
        game = BowlingGame()
        game.roll(10)
        self.assertEqual(game.score(), 10)
    
    def test_unfinished_game_with_spare(self):
        """Testing an unfinished valid game scenario where a spare happens in the first frame, 
        followed by one more frame played.
        
        Frames and scoring:
        Frame 1: 7, 3
        Frame 2: 4, 2
        
        Total expected score: 20
        """
        game = BowlingGame()
        game.roll(7)
        game.roll(3)
        game.roll(4)
        game.roll(2)
        self.assertEqual(game.score(), 20)
        
    def test_unfinished_regular_game(self):
        """Testing an unfinished valid game scenario where two full frames are played with no strikes or spares.
        
        Frames and scoring:
        Frame 1: 6, 3
        Frame 2: 4, 2
        
        Total expected score: 15
        """
        game = BowlingGame()
        game.roll(6)
        game.roll(3)
        game.roll(4)
        game.roll(2)
        self.assertEqual(game.score(), 15)

if __name__ == "__main__":
    unittest.main()