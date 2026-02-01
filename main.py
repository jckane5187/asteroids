import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_FONT, TITLE_FONT, MENU_FONT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scoreboard
from utils import set_game_state

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
    field = AsteroidField()
    game_state = "MENU"
    state_flags = {"menu_active": False, "round_active": False, "game_over_active": False}
    round_active = False
    menu_active = False
    game_over_active = False
    menu_ui_elements = {}
    game_over_ui_elements = {}
    clicked_quit = False
    clicked_play = False
    player = None
    score = None

    game_state, player, score, asteroids, shots, menu_ui_elements = \
        set_game_state("MENU", player, score, asteroids, shots, menu_ui_elements)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    while True:
        log_state()
        for event in pygame.event.get(): # event handling
            if event.type == pygame.QUIT:
                return
            
            if game_state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_ui_elements["menu_quit_rect"].collidepoint(event.pos):
                        clicked_quit = True
                    elif menu_ui_elements["menu_play_rect"].collidepoint(event.pos):
                        clicked_play = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if menu_ui_elements["menu_quit_rect"].collidepoint(event.pos) and clicked_quit:
                        clicked_quit = False
                        return
                    elif menu_ui_elements["menu_play_rect"].collidepoint(event.pos) and clicked_play:
                        clicked_play = False
                        game_state, player, score, asteroids, shots = \
                            set_game_state("PLAYING", player, score, asteroids, shots)
                    else:
                        clicked_play = False
                        clicked_quit = False

            elif game_state == "PLAYING":
                pass

            elif game_state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_over_ui_elements["menu_quit_rect"].collidepoint(event.pos):
                        clicked_quit = True
                    elif game_over_ui_elements["menu_play_rect"].collidepoint(event.pos):
                        clicked_play = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if game_over_ui_elements["menu_quit_rect"].collidepoint(event.pos) and clicked_quit:
                        clicked_quit = False
                        return
                    elif game_over_ui_elements["menu_play_rect"].collidepoint(event.pos) and clicked_play:
                        clicked_play = False
                        for roid in asteroids:
                            roid.kill()
                        game_state, player, score, asteroids, shots = \
                            set_game_state("PLAYING", player, score, asteroids, shots)
                        round_active = False
                    else:
                        clicked_play = False
                        clicked_quit = False

            else:
                raise Exception(f"Invalid game_state: {game_state}")
            
        # this is for updates
        updatable.update(dt)
        if game_state == "MENU": 
            pass

        elif game_state == "PLAYING":
            if round_active == False:
                score = Scoreboard()
                player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), scoreboard_ref=score)
                round_active = True
            for roid in asteroids:
                if player.collides_with(roid):
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Final Score: {score.score:.0f}")
                    player.kill()
                    for shot in shots:
                        shot.kill()
                    game_state, player, score, asteroids, shots, game_over_ui_elements = \
                        set_game_state("GAME_OVER", player, score, asteroids, shots, game_over_ui_elements)
                    round_active = False
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

        elif game_state == "GAME_OVER":
            pass

        else:
            raise Exception(f"Invalid game_state: {game_state}")

        # this is for drawing
        screen.fill("black")
        for ob in drawable:
            ob.draw(screen)

        if game_state == "MENU":
            screen.blit(menu_ui_elements["title_surface"], menu_ui_elements["title_rect"])
            screen.blit(menu_ui_elements["menu_play"], menu_ui_elements["menu_play_rect"])
            screen.blit(menu_ui_elements["menu_quit"], menu_ui_elements["menu_quit_rect"])

        elif game_state == "PLAYING":
            score_surface = SCORE_FONT.render(f"Score: {score.score:.0f}", True, "white")
            multi_surface = SCORE_FONT.render(f"Multi: {score.consecutive_multi:.1f}x", True, "white")
            screen.blit(score_surface, (0,0))
            screen.blit(multi_surface, (0,27))
            pass

        elif game_state == "GAME_OVER":
            screen.blit(game_over_ui_elements["title_surface"], game_over_ui_elements["title_rect"])
            screen.blit(game_over_ui_elements["menu_play"], game_over_ui_elements["menu_play_rect"])
            screen.blit(game_over_ui_elements["menu_quit"], game_over_ui_elements["menu_quit_rect"])

        else:
            raise Exception(f"Invalid game_state: {game_state}")
       
        pygame.display.flip()
        clock.tick(60)
        dt = (clock.tick(60) / 1000)


if __name__ == "__main__":
    main()
