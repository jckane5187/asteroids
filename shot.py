import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH
from utils import kill_offscreen
from logger import log_event

class Shot(CircleShape):
    next_id = 0

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.id = Shot.next_id
        Shot.next_id += 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        if kill_offscreen(self.position.x, self.position.y, self):
            log_event(f"shot {self.id} missed!")
