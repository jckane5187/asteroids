import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scoreboard
from utils import kill_offscreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Shot.containers = (shots, drawable, updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    score = Scoreboard()
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), scoreboard_ref=score)
    field = AsteroidField()
    score_font = pygame.font.Font(None, 36)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for ob in drawable:
            ob.draw(screen)
        for roid in asteroids:
            if player.collides_with(roid):
                log_event("player_hit")
                print("Game over!")
                print(f"Final Score: {score.score:.0f}")
                sys.exit()
        for shot in list(shots):
            hit_asteroid = None
            for roid in asteroids:
                if shot.collides_with(roid):
                    hit_asteroid = roid
                    break
            if hit_asteroid:
                log_event("asteroid_shot")
                score.consecutive_multi_increase(hit_asteroid.radius)
                score.asteroid_destroyed_score(hit_asteroid.radius)
                hit_asteroid.asteroid_split()
                shot.kill()
        score_surface = score_font.render(f"Score: {score.score:.0f}", True, "white")
        screen.blit(score_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)
        dt = (clock.tick(60) / 1000)


if __name__ == "__main__":
    main()
