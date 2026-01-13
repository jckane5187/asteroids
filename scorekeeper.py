from constants import POINTS_PER_KILL, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS

class Scoreboard():
    def __init__(self):
        self.score = 0
    
    def asteroid_destroyed_score(self, radius):
        self.score += POINTS_PER_KILL * (((ASTEROID_MAX_RADIUS - radius) // ASTEROID_MIN_RADIUS) + 1)