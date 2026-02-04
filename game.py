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
        self.field = AsteroidField()
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

            elif self.game_state == "PLAYING":
                pass

            elif self.game_state == "GAME_OVER":
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

            else:
                raise Exception(f"Invalid game_state: {self.game_state}")