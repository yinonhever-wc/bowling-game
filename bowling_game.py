"""
Bowling Game Implementation
A module for managing the bowling game, tracking its frames and rolls
and calculating its score.
"""

class BowlingGame:
    """This class represents a single game of bowling. It contains the data of the game's frames and roll in each frame;
    a method to add a new roll to the game; a method to calculate the game's total score; and utility methods to get the
    current frame, check a roll's validity, determine whether a strike or a spare was achieved in a certain frame, and 
    calculate the bonus a frame should receive for a strike or a frame."""
    
    def __init__(self):
        """
        The constructor initializes the list of frames, where each item inside it is a list of integers,
        representing the pins achieved in each roll in the frame.
        The game is initialized with one empty frame.
        """
        self.frames: list[list[int]] = [[]]

    def roll(self, pins: int):
        """
        This method receives a number of pins as a parameter and attempts to add a roll with that number of pins
        to the game's current frame.
        
        It first checks if the attempted roll is invalid - if the game has already ended, if the pins number is outside
        the valid range, or if the roll would result in an invalid pins total for the frame - and if so, it throws an
        appropriate error.
        
        If the roll is valid, it proceeds to add the roll to the current frame. If the frame ends after this new roll and it's
        not the 10th frame, it then adds a new empty frame to the game.
        """        
        is_roll_valid, roll_error = self._check_roll_validity(pins)
        if not is_roll_valid:
            raise roll_error or Exception("Invalid roll")
        
        current_frame, current_frame_order = self._get_current_frame()
            
        current_frame.append(pins)
        
        if current_frame_order < 10:
            if pins == 10 or len(current_frame) >= 2:
                self.frames.append([])
                
    def _check_roll_validity(self, pins: int) -> tuple[bool, Exception | None]:
        """
        This method receives a number of pins (an integer) as a parameter, and checks whether that roll
        is valid in the current context of the game. The method returns a tuple made of a boolean indicating whether 
        the roll is valid, and a custom error object if it's invalid.
        
        It first checks if the game has already ended, which is the case if the 10th frame is the current one and it already
        contains more than 2 rolls, or contains 2 rolls without a strike or a spare. In that case the attempted roll is marked 
        as invalid with a GameEndedError.
        
        Then it checks if the number of pins is in the valid range of 0 to 10, and if not, it marks the roll as invalid
        with an InvalidPinsError.
        
        Finally, it checks if that number of pins would result in an invalid pins total (higher than 10) for the current 
        frame, in which case the roll is marked as invalid with an InvalidPinsTotalInFrameError.
        If the current frame is a regular one (one of the first 9 frames), the code simply checks whether the frame's total 
        pins would be higher than 10 after this roll.
        If the current frame is the 10th one (where an extra roll is given in case all 10 rolls are knocked), the code allows
        a total higher than 10 in certain scenarios and combinations, depending on whether a strike or a spare has been 
        achieved on the frame, and on which roll. 
        """
        current_frame, current_frame_order = self._get_current_frame()

        if current_frame_order >= 10:
            if len(current_frame) > 2 or (len(current_frame) == 2 and sum(current_frame) < 10):
                return False, GameEndedError()
            
        if pins < 0 or pins > 10:
            return False, InvalidPinsError()
                
        if current_frame_order < 10:
            if sum(current_frame) + pins > 10:
                return False, InvalidPinsTotalInFrameError()
        else:
            if len(current_frame) == 2 and current_frame[0] == 10 and current_frame[1] == 10:
                pass  # two strikes: roll 3 is fully fresh, no check needed
            elif len(current_frame) == 2 and sum(current_frame) == 10:
                pass  # spare: roll 3 is fresh, no check needed
            elif len(current_frame) == 1 and current_frame[0] == 10:
                pass  # roll 1 roll was a strike: roll 2 is fresh
            elif len(current_frame) == 2 and current_frame[0] == 10:
                # roll 1 was a strike, roll 2 wasn't: roll 3 only needs to fit with roll 2
                if current_frame[1] + pins > 10:
                    return False, InvalidPinsTotalInFrameError()
            elif sum(current_frame) + pins > 10:
                return False, InvalidPinsTotalInFrameError()
        
        return True, None
    
    def _get_current_frame(self):
        """
        This method returns a tuple containing the current frame (a list of integers) that's currently being played,
        and number representing the order of that frame in the game (1 to 10).
        """
        current_frame = self.frames[-1]
        current_frame_order = len(self.frames)
        return current_frame, current_frame_order

    def score(self):
        """
        This method calculates and returns the total score for all the frames that have been played in the game.
        It loops through each frame, adds the sum of its rolls to the total score, and adds the appropriate bonus
        if a strike or a spare was achieved in the frame.
        """
        score = 0

        for frame_index in range(len(self.frames)):
            frame = self.frames[frame_index]
            score += sum(frame)
            
            if self._is_strike(frame_index):
                score += self._strike_bonus(frame_index)
            elif self._is_spare(frame_index):
                score += self._spare_bonus(frame_index)

        return score

    def _is_strike(self, frame_index: int):
        """
        This method receives a frame's index as a parameter and returns a boolean indicating whether a strike was
        achieved in that frame (whether it contains a roll of 10) and it's not the 10th frame.
        """
        return frame_index + 1 < len(self.frames) and 10 in self.frames[frame_index]

    def _is_spare(self, frame_index: int):
        """
        This method receives a frame's index as a parameter and returns a boolean indicating whether a spare was
        achieved in that frame (whether its rolls have a total of 10 pins but without a single roll of 10) and it's
        not the 10th frame.
        """
        frame = self.frames[frame_index]
        return frame_index + 1 < len(self.frames) and sum(frame) == 10 and 10 not in frame

    def _strike_bonus(self, frame_index: int):
        """
        This receives a frame's index as a parameter and returns the bonus that frame should receive for a strike.
        The bonus is calculated as the total pins of the next two rolls after that frame, if two subsequent rolls have 
        already been played. If only one subsequent roll has been played so far, the bonus is that single roll's pins.
        If no subsquent rolls have been played yet, the bonus is 0.
        """
        next_frame = self.frames[frame_index + 1]
        if not next_frame:
            return 0
        if len(next_frame) >= 2:
            return sum(next_frame[:2])
        try:
            return next_frame[0] + self.frames[frame_index + 2][0]
        except IndexError:
            return next_frame[0]

    def _spare_bonus(self, frame_index: int):
        """
        This receives a frame's index as a parameter and returns the bonus that frame should receive for a spare.
        The bonus is the number of pins in the roll played after that frame, or 0 if no subsequent roll has been played yet.
        """
        next_frame = self.frames[frame_index + 1]
        return next_frame[0] if next_frame else 0


class GameEndedError(Exception):
    """This class represents an error object that should be raised in case of an attempt to roll
    when the game has already ended."""
    
    def __init__(self, message="Can't roll any more, game has ended."):
        self.message = message
        super().__init__(self.message)


class InvalidPinsError(Exception):
    """This class represents an error object that should be raised in case of an attempt to roll
    an invalid number of pins, outside the valid range of 0 to 10."""
    
    def __init__(self, message="Invalid roll - pins must be between 0 and 10."):
        self.message = message
        super().__init__(self.message)


class InvalidPinsTotalInFrameError(Exception):
    """This class represents an error object that should be raised in case an attempted roll would result
    in an invalid pins total for the current frame."""
    
    def __init__(self, message="""Invalid roll - total pins in a frame can't be more than 10, 
                 unless an extra roll was gained in the last frame."""):
        self.message = message
        super().__init__(self.message)