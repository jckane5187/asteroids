from constants import POINTS_PER_KILL

class Scoreboard():
    def __init__(self):
        self.score = 0
    
    def asteroid_destroyed_score(self):
        self.score += POINTS_PER_KILL