from constants import POINTS_PER_KILL, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, MAX_CONSEC_SHOT_MULTI, BASE_CONSEC_SHOT_MULTI_INC

class Scoreboard():
    def __init__(self):
        self.score = 0
        self.consecutive_multi = 1
    
    def asteroid_destroyed_score(self, radius):
        self.score += POINTS_PER_KILL * (((ASTEROID_MAX_RADIUS - radius) // ASTEROID_MIN_RADIUS) + 1) * self.consecutive_multi

    def consecutive_multi_increase(self, radius):
        potential_new_multiplier = self.consecutive_multi + (BASE_CONSEC_SHOT_MULTI_INC * (((ASTEROID_MAX_RADIUS - radius) // ASTEROID_MIN_RADIUS) + 1))
        self.consecutive_multi = min(potential_new_multiplier, MAX_CONSEC_SHOT_MULTI)
        print(self.consecutive_multi)

    def reset_consecutive_multi(self):
        self.consecutive_multi = 1