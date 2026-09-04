"""
Bowling Game Implementation
A module for calculating bowling game scores.
"""

class BowlingGame:
    def __init__(self):
        # Initialize a new game with 10 frames
        # Each frame has up to 2 rolls (except the 10th frame which can have 3)
        self.frames = [[]]

    def roll(self, pins: int):
        
        current_frame, current_frame_order = self._get_current_frame()

        if current_frame_order >= 10:
            if len(current_frame) > 2 or (len(current_frame) == 2 and sum(current_frame) < 10):
                raise Exception("Can't roll any more, game has ended.")
        
        if not self._is_valid_roll(pins):
            raise Exception("""Invalid roll - pins must be between 0-10, and total pins in a frame can't be more than 10, 
                            unless an extra roll was gained in the last frame.""")
            
        current_frame.append(pins)
        
        if current_frame_order < 10:
            if pins == 10 or len(current_frame) >= 2:
                self.frames.append([])
                
    def _is_valid_roll(self, pins: int) -> bool:
        
        if pins < 0 or pins > 10:
            return False
        
        current_frame, current_frame_order = self._get_current_frame()
        
        if current_frame_order < 10:
            if sum(current_frame) + pins > 10:
                return False
        else:
            if len(current_frame) == 2 and current_frame[0] == 10 and current_frame[1] == 10:
                pass  # two strikes: roll 3 is fully fresh, no check needed
            elif len(current_frame) == 2 and sum(current_frame) == 10:
                pass  # spare: roll 3 is fresh, no check needed
            elif len(current_frame) == 1 and current_frame[0] == 10:
                pass  # roll 1 roll was a strike: roll 2 is fresh
            elif sum(current_frame) + pins > 10:
                return False
        
        return True
    
    def _get_current_frame(self):
        current_frame = self.frames[-1]
        current_frame_order = len(self.frames)
        return (current_frame, current_frame_order)

    def score(self):
        
        score = 0

        for frame_index in range(len(self.frames)):
            frame = self.frames[frame_index]
            score += sum(frame)
            
            if self._is_strike(frame_index):
                # Strike
                score += self._strike_bonus(frame_index)
            elif self._is_spare(frame_index):
                # Spare
                score += self._spare_bonus(frame_index)

        return score

    def _is_strike(self, frame_index: int):
        
        return frame_index + 1 < len(self.frames) and 10 in self.frames[frame_index]

    def _is_spare(self, frame_index: int):
        
        frame = self.frames[frame_index]
        return frame_index + 1 < len(self.frames) and sum(frame) == 10 and 10 not in frame

    def _strike_bonus(self, frame_index: int):
       
        next_frame = self.frames[frame_index + 1]
        if len(next_frame) >= 2:
            return sum(next_frame[:2])
        return next_frame[0] + self.frames[frame_index + 2][0]

    def _spare_bonus(self, frame_index: int):
       
        return self.frames[frame_index + 1][0]