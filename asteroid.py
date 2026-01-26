import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_WRAP_SPAWN_TIMER
from logger import log_event
from utils import position_wrap

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.wrap_timer = ASTEROID_WRAP_SPAWN_TIMER

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        if self.wrap_timer > 0:
            self.wrap_timer -= dt
        self.position += self.velocity * dt
        if self.wrap_timer < 0:
            self.position.x, self.position.y = position_wrap(self.position.x, self.position.y)

    def asteroid_split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        rotate_velocity1 = self.velocity.rotate(angle)
        rotate_velocity2 = self.velocity.rotate(-angle)
        smol_rad = self.radius - ASTEROID_MIN_RADIUS
        roid1 = Asteroid(self.position, self.position, smol_rad)
        roid1.velocity = rotate_velocity1 * 1.2
        roid2 = Asteroid(self.position, self.position, smol_rad)
        roid2.velocity = rotate_velocity2 * 1.2