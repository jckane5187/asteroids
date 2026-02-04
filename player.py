import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot
from utils import position_wrap

class Player(CircleShape):
    def __init__(self, x, y, scoreboard_ref):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.scoreboard = scoreboard_ref
        self.rotating_left = False
        self.rotating_right = False
        self.accelerating_forward = False
        self.accelerating_backward = False
        self.shooting = False
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation = self.rotation + (PLAYER_TURN_SPEED * dt)
    
    def update(self, dt):
        self.shot_cooldown -= dt

        if self.rotating_left:
            self.rotate(-dt)
        
        if self.rotating_right:
            self.rotate(dt)

        if self.accelerating_forward:
            self.move(dt)

        if self.accelerating_backward:
            self.move(-dt)

        if self.shooting:
            if self.shot_cooldown > 0:
                return
            self.shoot()
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        self.position.x, self.position.y = position_wrap(self.position.x, self.position.y)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed

    def shoot(self):
        bullet = Shot(self.position, self.position, SHOT_RADIUS, self.scoreboard)
        base_vel = pygame.Vector2(0, 1)
        rotated_vel = base_vel.rotate(self.rotation)
        bullet.velocity = rotated_vel * PLAYER_SHOOT_SPEED
    
    def start_rotating_left(self):
        self.rotating_left = True
    
    def stop_rotating_left(self):
        self.rotating_left = False

    def start_rotating_right(self):
        self.rotating_right = True
    
    def stop_rotating_right(self):
        self.rotating_right = False

    def start_accelerating_forward(self):
        self.accelerating_forward = True
    
    def stop_accelerating_forward(self):
        self.accelerating_forward = False

    def start_accelerating_backward(self):
        self.accelerating_backward = True
    
    def stop_accelerating_backward(self):
        self.accelerating_backward = False

    def start_shooting(self):
        self.shooting = True
    
    def stop_shooting(self):
        self.shooting = False
