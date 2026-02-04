import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_FONT, TITLE_FONT, MENU_FONT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scoreboard

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.game_state = "MENU"
        self.menu_ui_elements = {}
        self.game_over_ui_elements = {}
        self.clicked_quit = False
        self.clicked_play = False
        self.player = None
        self.score = None
        Shot.containers = (self.shots, self.drawable, self.updatable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Player.containers = (self.updatable, self.drawable)
        self.field = AsteroidField()
        self.set_state("MENU")
        self._quit_game = False
        
        print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")

    def set_state(self, new_state):
        self.game_state = new_state

        if new_state == "MENU":
            self.menu_ui_elements.clear()

            self.menu_ui_elements["title_surface"] = TITLE_FONT.render("ASTEROIDS", True, "white")
            self.menu_ui_elements["title_rect"] = self.menu_ui_elements["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

            self.menu_ui_elements["menu_play"] = MENU_FONT.render("PLAY", True, "white")
            self.menu_ui_elements["menu_play_rect"] = self.menu_ui_elements["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            self.menu_ui_elements["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
            self.menu_ui_elements["menu_quit_rect"] = self.menu_ui_elements["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.menu_ui_elements["menu_quit_rect"].top = self.menu_ui_elements["menu_play_rect"].bottom + 36

            for roid in self.asteroids:
                roid.kill()
            self.shots.empty()
            self.player = None
            self.score = None

        elif new_state == "PLAYING":
            for roid in self.asteroids:
                roid.kill()
            self.shots.empty()
            self.score = Scoreboard()
            self.player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), scoreboard_ref=self.score)
            

        elif new_state == "GAME_OVER":
            self.game_over_ui_elements.clear()
            
            self.game_over_ui_elements["title_surface"] = TITLE_FONT.render("GAME OVER", True, "white")
            self.game_over_ui_elements["title_rect"] = self.game_over_ui_elements["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

            self.game_over_ui_elements["final_score_surface"] = MENU_FONT.render(f"Final Score: {self.score.score:.0f}", True, "white")
            self.game_over_ui_elements["final_score_rect"] = self.game_over_ui_elements["final_score_surface"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.game_over_ui_elements["final_score_rect"].top = self.game_over_ui_elements["title_rect"].bottom

            self.game_over_ui_elements["menu_play"] = MENU_FONT.render("PLAY", True, "white")
            self.game_over_ui_elements["menu_play_rect"] = self.game_over_ui_elements["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            self.game_over_ui_elements["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
            self.game_over_ui_elements["menu_quit_rect"] = self.game_over_ui_elements["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.game_over_ui_elements["menu_quit_rect"].top = self.game_over_ui_elements["menu_play_rect"].bottom + 36
        
        else:
            raise Exception(f"Invalid game_state: {new_state}")
        
    def run(self):
        while True:
            self._handle_input()
            self._update()
            self._draw()
            self._tick()

            if self._quit_game:
                return
    
    def _tick(self):
        self.dt = (self.clock.tick(60) / 1000)

    def _handle_input(self):
        for event in pygame.event.get(): # event handling
            if event.type == pygame.QUIT:
                return
            
            if self.game_state == "MENU":
                self._handle_menu_input(event)

            elif self.game_state == "PLAYING":
                self._handle_playing_input(event)

            elif self.game_state == "GAME_OVER":
                self._handle_game_over_input(event)

            else:
                raise Exception(f"Invalid game_state: {self.game_state}")
    
    def _handle_menu_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_ui_elements["menu_quit_rect"].collidepoint(event.pos):
                self.clicked_quit = True
            elif self.menu_ui_elements["menu_play_rect"].collidepoint(event.pos):
                self.clicked_play = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.menu_ui_elements["menu_quit_rect"].collidepoint(event.pos) and self.clicked_quit:
                self.clicked_quit = False
                self._quit_game = True
                return
            elif self.menu_ui_elements["menu_play_rect"].collidepoint(event.pos) and self.clicked_play:
                self.clicked_play = False
                self.set_state("PLAYING")
            else:
                self.clicked_play = False
                self.clicked_quit = False
    
    def _handle_playing_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.start_rotating_left()
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.start_rotating_right()
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.start_accelerating_forward()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.player.start_accelerating_backward()
            elif event.key == pygame.K_SPACE:
                self.player.start_shooting()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.stop_rotating_left()
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.stop_rotating_right()
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.stop_accelerating_forward()
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.player.stop_accelerating_backward()
            elif event.key == pygame.K_SPACE:
                self.player.stop_shooting()

    def _handle_game_over_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_over_ui_elements["menu_quit_rect"].collidepoint(event.pos):
                self.clicked_quit = True
            elif self.game_over_ui_elements["menu_play_rect"].collidepoint(event.pos):
                self.clicked_play = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.game_over_ui_elements["menu_quit_rect"].collidepoint(event.pos) and self.clicked_quit:
                self.clicked_quit = False
                self._quit_game = True
                return
            elif self.game_over_ui_elements["menu_play_rect"].collidepoint(event.pos) and self.clicked_play:
                self.clicked_play = False
                for roid in self.asteroids:
                    roid.kill()
                self.set_state("PLAYING")
            else:
                self.clicked_play = False
                self.clicked_quit = False
    
    def _update(self):
        log_state()
        self.updatable.update(self.dt)
        if self.game_state == "MENU": 
            pass

        elif self.game_state == "PLAYING":
            for roid in self.asteroids:
                if self.player.collides_with(roid):
                    log_event("player_hit")
                    self.player.kill()
                    for shot in self.shots:
                        shot.kill()
                    self.set_state("GAME_OVER")
                    return
            for shot in list(self.shots):
                hit_asteroid = None
                for roid in self.asteroids:
                    if shot.collides_with(roid):
                        hit_asteroid = roid
                        break
                if hit_asteroid:
                    log_event("asteroid_shot")
                    self.score.consecutive_multi_increase(hit_asteroid.radius)
                    self.score.asteroid_destroyed_score(hit_asteroid.radius)
                    hit_asteroid.asteroid_split()
                    shot.kill()

        elif self.game_state == "GAME_OVER":
            pass

        else:
            raise Exception(f"Invalid game_state: {self.game_state}")

    def _draw(self):
        self.screen.fill("black")
        for ob in self.drawable:
            ob.draw(self.screen)

        if self.game_state == "MENU":
            self.screen.blit(self.menu_ui_elements["title_surface"], self.menu_ui_elements["title_rect"])
            self.screen.blit(self.menu_ui_elements["menu_play"], self.menu_ui_elements["menu_play_rect"])
            self.screen.blit(self.menu_ui_elements["menu_quit"], self.menu_ui_elements["menu_quit_rect"])

        elif self.game_state == "PLAYING":
            score_surface = SCORE_FONT.render(f"Score: {self.score.score:.0f}", True, "white")
            multi_surface = SCORE_FONT.render(f"Multi: {self.score.consecutive_multi:.1f}x", True, "white")
            self.screen.blit(score_surface, (0,0))
            self.screen.blit(multi_surface, (0,27))
            pass

        elif self.game_state == "GAME_OVER":
            self.screen.blit(self.game_over_ui_elements["title_surface"], self.game_over_ui_elements["title_rect"])
            self.screen.blit(self.game_over_ui_elements["final_score_surface"], self.game_over_ui_elements["final_score_rect"])
            self.screen.blit(self.game_over_ui_elements["menu_play"], self.game_over_ui_elements["menu_play_rect"])
            self.screen.blit(self.game_over_ui_elements["menu_quit"], self.game_over_ui_elements["menu_quit_rect"])

        else:
            raise Exception(f"Invalid game_state: {self.game_state}")
       
        pygame.display.flip()