from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, SIZE_SMALL, SIZE_LARGE, SIZE_MEDIUM

class Round():
    round_number = 1
    
    def __init__(self):
        self.round_time = 0 # seconds
        self.round_score = 0
        self.round_asteroids_destroyed = 0
        self.round_asteroids_destroyed_by_size = {SIZE_SMALL: 0, SIZE_MEDIUM: 0, SIZE_LARGE: 0}
        self.round_shots_fired = 0
        self.longest_consecutive_shot_chain = 0
        self.current_shot_chain = 0
        self.round_number = Round.round_number
        Round.round_number += 1

    def time_elapsed(self, dt):
        self.round_time += dt

    def set_score(self, score):
        self.round_score = score

    def increase_shot_fired(self):
        self.round_shots_fired += 1
    
    def increase_shot_chain(self):
        self.current_shot_chain += 1

    def compare_longest_chain_and_reset(self):
        if self.current_shot_chain > self.longest_consecutive_shot_chain:
            self.longest_consecutive_shot_chain = self.current_shot_chain
        self.current_shot_chain = 0

    def update_asteroid_destroyed(self, radius):
        self.round_asteroids_destroyed += 1
        size_key = None
        if radius == ASTEROID_MIN_RADIUS:
            size_key = SIZE_SMALL
        elif radius > ASTEROID_MIN_RADIUS and radius < ASTEROID_MAX_RADIUS:
            size_key = SIZE_MEDIUM
        elif radius == ASTEROID_MAX_RADIUS:
            size_key = SIZE_LARGE
        else:
            raise Exception(f"invalid asteroid size detected: {radius}")

        self.round_asteroids_destroyed_by_size[size_key] += 1