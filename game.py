import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCORE_FONT, TITLE_FONT, MENU_FONT, SAVE_FILE, SIZE_SMALL, SIZE_MEDIUM, SIZE_LARGE
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scorekeeper import Scoreboard
from playerdata import PlayerData
from round import Round
from utils import kill_offscreen

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
        self.stats_ui_elements = {}
        self.clicked_quit = False
        self.clicked_play = False
        self.clicked_stats = False
        self.clicked_return = False
        self.player = None
        self.score = None
        self.current_round = None
        self.previous_state = None
        Shot.containers = (self.shots, self.drawable, self.updatable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable)
        Player.containers = (self.updatable, self.drawable)
        self.field = AsteroidField()
        self.player_data = PlayerData.load_data(SAVE_FILE)
        self.set_state("MENU")
        self._quit_game = False
        
        print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
        print(f"Screen width: {SCREEN_WIDTH}")
        print(f"Screen height: {SCREEN_HEIGHT}")

    def set_state(self, new_state):
        self.previous_state = self.game_state
        self.game_state = new_state

        if new_state == "MENU":
            self.menu_ui_elements.clear()

            self.menu_ui_elements["title_surface"] = TITLE_FONT.render("ASTEROIDS", True, "white")
            self.menu_ui_elements["title_rect"] = self.menu_ui_elements["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

            self.menu_ui_elements["menu_play"] = MENU_FONT.render("PLAY", True, "white")
            self.menu_ui_elements["menu_play_rect"] = self.menu_ui_elements["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            self.menu_ui_elements["menu_stats"] = MENU_FONT.render("STATS", True, "white")
            self.menu_ui_elements["menu_stats_rect"] = self.menu_ui_elements["menu_stats"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.menu_ui_elements["menu_stats_rect"].top = self.menu_ui_elements["menu_play_rect"].bottom + 36

            self.menu_ui_elements["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
            self.menu_ui_elements["menu_quit_rect"] = self.menu_ui_elements["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.menu_ui_elements["menu_quit_rect"].top = self.menu_ui_elements["menu_stats_rect"].bottom + 36

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
            self.current_round = Round()
            self.player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
            
            log_event(f"round {self.current_round.round_number} started")
            

        elif new_state == "GAME_OVER":
            self.game_over_ui_elements.clear()
            
            self.game_over_ui_elements["title_surface"] = TITLE_FONT.render("GAME OVER", True, "white")
            self.game_over_ui_elements["title_rect"] = self.game_over_ui_elements["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))

            self.game_over_ui_elements["final_score_surface"] = MENU_FONT.render(f"Final Score: {self.score.score:.0f}", True, "white")
            self.game_over_ui_elements["final_score_rect"] = self.game_over_ui_elements["final_score_surface"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.game_over_ui_elements["final_score_rect"].top = self.game_over_ui_elements["title_rect"].bottom

            self.game_over_ui_elements["menu_play"] = MENU_FONT.render("PLAY", True, "white")
            self.game_over_ui_elements["menu_play_rect"] = self.game_over_ui_elements["menu_play"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            self.game_over_ui_elements["menu_stats"] = MENU_FONT.render("STATS", True, "white")
            self.game_over_ui_elements["menu_stats_rect"] = self.menu_ui_elements["menu_stats"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.game_over_ui_elements["menu_stats_rect"].top = self.menu_ui_elements["menu_play_rect"].bottom + 36

            self.game_over_ui_elements["menu_quit"] = MENU_FONT.render("QUIT", True, "white")
            self.game_over_ui_elements["menu_quit_rect"] = self.game_over_ui_elements["menu_quit"].get_rect(centerx=(SCREEN_WIDTH / 2))
            self.game_over_ui_elements["menu_quit_rect"].top = self.game_over_ui_elements["menu_stats_rect"].bottom + 36

        elif new_state == "STATS": # depending on the size, this may require the ability to scroll through through the stats. I will initially try to keep it
            # to a small enough area, but need to be prepared to either learn how to do it, or download a library to handle it for me
            self.stats_ui_elements.clear()
            # templates
            # self.stats_ui_elements["thing"] = font_constant.render("WORD", True, "White")
            # self.stats_ui_elements["thing_rect"] = self.stats_ui_elements["thing"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["title_surface"] = TITLE_FONT.render("STATS", True, "White")
            self.stats_ui_elements["title_rect"] = self.stats_ui_elements["title_surface"].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8))

            # Total Stats
            self.stats_ui_elements["combined_stats_surface"] = MENU_FONT.render("Combined Stats", True, "White")
            self.stats_ui_elements["combined_stats_surface_rect"] = self.stats_ui_elements["combined_stats_surface"].get_rect(center=(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))

            self.stats_ui_elements["total_time_played_surface"] = SCORE_FONT.render(f"Time Played: {self.player_data.total_time_played:.0f}", True, "White")
            self.stats_ui_elements["total_time_played_surface_rect"] = self.stats_ui_elements["total_time_played_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_time_played_surface_rect"].top = self.stats_ui_elements["combined_stats_surface_rect"].bottom + 12

            self.stats_ui_elements["total_rounds_played_surface"] = SCORE_FONT.render(f"Rounds Played: {self.player_data.total_rounds_played}", True, "White")
            self.stats_ui_elements["total_rounds_played_surface_rect"] = self.stats_ui_elements["total_rounds_played_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_rounds_played_surface_rect"].top = self.stats_ui_elements["total_time_played_surface_rect"].bottom + 12

            self.stats_ui_elements["total_score_earned_surface"] = SCORE_FONT.render(f"Score Earned: {self.player_data.total_score_earned:.0f}", True, "White")
            self.stats_ui_elements["total_score_earned_surface_rect"] = self.stats_ui_elements["total_score_earned_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_score_earned_surface_rect"].top = self.stats_ui_elements["total_rounds_played_surface_rect"].bottom + 12

            self.stats_ui_elements["total_shots_fired_surface"] = SCORE_FONT.render(f"Shots Fired: {self.player_data.total_shots_fired}", True, "White")
            self.stats_ui_elements["total_shots_fired_surface_rect"] = self.stats_ui_elements["total_shots_fired_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_shots_fired_surface_rect"].top = self.stats_ui_elements["total_score_earned_surface_rect"].bottom + 12

            self.stats_ui_elements["total_roids_destroyed_surface"] = SCORE_FONT.render(f"Asteroids Destroyed: {self.player_data.total_asteroids_destroyed}", True, "White")
            self.stats_ui_elements["total_roids_destroyed_surface_rect"] = self.stats_ui_elements["total_roids_destroyed_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_roids_destroyed_surface_rect"].top = self.stats_ui_elements["total_shots_fired_surface_rect"].bottom + 12

            self.stats_ui_elements["total_small_destroyed_surface"] = SCORE_FONT.render(f"Small: {self.player_data.asteroids_destroyed_by_size[SIZE_SMALL]}", True, "White")
            self.stats_ui_elements["total_small_destroyed_surface_rect"] = self.stats_ui_elements["total_small_destroyed_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_small_destroyed_surface_rect"].top = self.stats_ui_elements["total_roids_destroyed_surface_rect"].bottom + 12

            self.stats_ui_elements["total_medium_destroyed_surface"] = SCORE_FONT.render(f"Medium: {self.player_data.asteroids_destroyed_by_size[SIZE_MEDIUM]}", True, "White")
            self.stats_ui_elements["total_medium_destroyed_surface_rect"] = self.stats_ui_elements["total_medium_destroyed_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_medium_destroyed_surface_rect"].top = self.stats_ui_elements["total_small_destroyed_surface_rect"].bottom + 12

            self.stats_ui_elements["total_large_destroyed_surface"] = SCORE_FONT.render(f"Large: {self.player_data.asteroids_destroyed_by_size[SIZE_LARGE]}", True, "White")
            self.stats_ui_elements["total_large_destroyed_surface_rect"] = self.stats_ui_elements["total_large_destroyed_surface"].get_rect(centerx=(SCREEN_WIDTH / 4))
            self.stats_ui_elements["total_large_destroyed_surface_rect"].top = self.stats_ui_elements["total_medium_destroyed_surface_rect"].bottom + 12

            # Best Single Round Stats
            self.stats_ui_elements["best_stats_surface"] = MENU_FONT.render("Best Single Round Stats", True, "White")
            self.stats_ui_elements["best_stats_surface_rect"] = self.stats_ui_elements["best_stats_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))

            self.stats_ui_elements["round_time_played_surface"] = SCORE_FONT.render(f"Longest Round: {self.player_data.longest_round:.0f}", True, "White")
            self.stats_ui_elements["round_time_played_surface_rect"] = self.stats_ui_elements["round_time_played_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["round_time_played_surface_rect"].top = self.stats_ui_elements["best_stats_surface_rect"].bottom + 12

            self.stats_ui_elements["best_score_surface"] = SCORE_FONT.render(f"Highest Score: {self.player_data.highest_single_round_score:.0f}", True, "White")
            self.stats_ui_elements["best_score_surface_rect"] = self.stats_ui_elements["best_score_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_score_surface_rect"].top = self.stats_ui_elements["round_time_played_surface_rect"].bottom + 12

            self.stats_ui_elements["best_shot_chain"] = SCORE_FONT.render(f"Longest Shot Chain: {self.player_data.longest_consecutive_shot_chain}", True, "White")
            self.stats_ui_elements["best_shot_chain_rect"] = self.stats_ui_elements["best_shot_chain"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_shot_chain_rect"].top = self.stats_ui_elements["best_score_surface_rect"].bottom + 12

            self.stats_ui_elements["best_roids_destroyed_surface"] = SCORE_FONT.render(f"Most Asteroids Destroyed: {self.player_data.most_asteroids_destroyed_single_round}", True, "White")
            self.stats_ui_elements["best_roids_destroyed_surface_rect"] = self.stats_ui_elements["best_roids_destroyed_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_roids_destroyed_surface_rect"].top = self.stats_ui_elements["best_shot_chain_rect"].bottom + 12

            self.stats_ui_elements["best_small_destroyed_surface"] = SCORE_FONT.render(f"Small: {self.player_data.most_asteroids_destroyed_by_size_single_round[SIZE_SMALL]}", True, "White")
            self.stats_ui_elements["best_small_destroyed_surface_rect"] = self.stats_ui_elements["best_small_destroyed_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_small_destroyed_surface_rect"].top = self.stats_ui_elements["best_roids_destroyed_surface_rect"].bottom + 12

            self.stats_ui_elements["best_medium_destroyed_surface"] = SCORE_FONT.render(f"Medium: {self.player_data.most_asteroids_destroyed_by_size_single_round[SIZE_MEDIUM]}", True, "White")
            self.stats_ui_elements["best_medium_destroyed_surface_rect"] = self.stats_ui_elements["best_medium_destroyed_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_medium_destroyed_surface_rect"].top = self.stats_ui_elements["best_small_destroyed_surface_rect"].bottom + 12

            self.stats_ui_elements["best_large_destroyed_surface"] = SCORE_FONT.render(f"Large: {self.player_data.most_asteroids_destroyed_by_size_single_round[SIZE_LARGE]}", True, "White")
            self.stats_ui_elements["best_large_destroyed_surface_rect"] = self.stats_ui_elements["best_large_destroyed_surface"].get_rect(center=(SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4))
            self.stats_ui_elements["best_large_destroyed_surface_rect"].top = self.stats_ui_elements["best_medium_destroyed_surface_rect"].bottom + 12

            # Clickable Button
            self.stats_ui_elements["stats_return"] = MENU_FONT.render("RETURN", True, "white")
            self.stats_ui_elements["stats_return_rect"] = self.stats_ui_elements["stats_return"].get_rect(center=(SCREEN_WIDTH * (7 / 8), SCREEN_HEIGHT * (9 / 10)))
            
        
        else:
            raise Exception(f"Invalid game_state: {new_state}")
        
    def run(self):
        running = True
        while running:
            self._handle_input()
            self._update()
            self._draw()
            self._tick()

            if self._quit_game:
                running = False
        
        self.player_data.save_data(SAVE_FILE)
        return
    
    def _tick(self):
        self.dt = (self.clock.tick(60) / 1000)

    def _handle_input(self):
        for event in pygame.event.get(): # event handling
            if event.type == pygame.QUIT:
                self._quit_game = True
                return
            
            if self.game_state == "MENU":
                self._handle_menu_input(event)

            elif self.game_state == "PLAYING":
                self._handle_playing_input(event)

            elif self.game_state == "GAME_OVER":
                self._handle_game_over_input(event)

            elif self.game_state == "STATS":
                self._handle_stats_input(event)

            else:
                raise Exception(f"Invalid game_state: {self.game_state}")
    
    def _handle_menu_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_ui_elements["menu_quit_rect"].collidepoint(event.pos):
                self.clicked_quit = True
            elif self.menu_ui_elements["menu_play_rect"].collidepoint(event.pos):
                self.clicked_play = True
            elif self.menu_ui_elements["menu_stats_rect"].collidepoint(event.pos):
                self.clicked_stats = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.menu_ui_elements["menu_quit_rect"].collidepoint(event.pos) and self.clicked_quit:
                self.clicked_quit = False
                self._quit_game = True
                return
            elif self.menu_ui_elements["menu_play_rect"].collidepoint(event.pos) and self.clicked_play:
                self.clicked_play = False
                self.set_state("PLAYING")
            elif self.menu_ui_elements["menu_stats_rect"].collidepoint(event.pos) and self.clicked_stats:
                self.clicked_stats = False
                self.set_state("STATS")
            else:
                self.clicked_play = False
                self.clicked_stats = False
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
            elif self.game_over_ui_elements["menu_stats_rect"].collidepoint(event.pos):
                self.clicked_stats = True
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
            elif self.game_over_ui_elements["menu_stats_rect"].collidepoint(event.pos) and self.clicked_stats:
                self.clicked_stats = False
                self.set_state("STATS")
            else:
                self.clicked_play = False
                self.clicked_stats = False
                self.clicked_quit = False

    def _handle_stats_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.stats_ui_elements["stats_return_rect"].collidepoint(event.pos):
                self.clicked_return = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.stats_ui_elements["stats_return_rect"].collidepoint(event.pos) and self.clicked_return:
                self.clicked_return = False
                self.set_state(self.previous_state)
                return
            else:
                self.clicked_return = False
    
    def _update(self):
        log_state()
        self.updatable.update(self.dt)
        if self.game_state == "MENU": 
            pass

        elif self.game_state == "PLAYING":
            self.current_round.time_elapsed(self.dt)
            if self.player.just_shot:
                self.current_round.increase_shot_fired()
                self.current_round.increase_shot_chain()
            for roid in self.asteroids:
                if self.player.collides_with(roid):
                    log_event("player_hit")
                    log_event(f"round {self.current_round.round_number} ended")
                    self.player.kill()
                    for shot in self.shots:
                        shot.kill()
                    self.current_round.compare_longest_chain_and_reset()
                    self.current_round.set_score(self.score.score)
                    self.player_data.collect_and_record_round_data(self.current_round)
                    self.player_data.save_data(SAVE_FILE)
                    self.set_state("GAME_OVER")
                    return
            for shot in list(self.shots):
                if kill_offscreen(shot.position.x, shot.position.y, shot):
                    self.score.reset_consecutive_multi()
                    log_event(f"shot {shot.id} missed! consecutive shot multi reset")
                    self.current_round.compare_longest_chain_and_reset()
                hit_asteroid = None
                for roid in self.asteroids:
                    if shot.collides_with(roid):
                        hit_asteroid = roid
                        break
                if hit_asteroid:
                    log_event("asteroid_shot")
                    self.score.consecutive_multi_increase(hit_asteroid.radius)
                    self.score.asteroid_destroyed_score(hit_asteroid.radius)
                    self.current_round.update_asteroid_destroyed(hit_asteroid.radius)
                    hit_asteroid.asteroid_split()
                    shot.kill()

        elif self.game_state == "GAME_OVER":
            pass

        elif self.game_state == "STATS":
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
            self.screen.blit(self.menu_ui_elements["menu_stats"], self.menu_ui_elements["menu_stats_rect"])
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
            self.screen.blit(self.game_over_ui_elements["menu_stats"], self.game_over_ui_elements["menu_stats_rect"])
            self.screen.blit(self.game_over_ui_elements["menu_quit"], self.game_over_ui_elements["menu_quit_rect"])

        elif self.game_state == "STATS":
            self.screen.blit(self.stats_ui_elements["title_surface"], self.stats_ui_elements["title_rect"])
            self.screen.blit(self.stats_ui_elements["stats_return"], self.stats_ui_elements["stats_return_rect"])
            self.screen.blit(self.stats_ui_elements["combined_stats_surface"], self.stats_ui_elements["combined_stats_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_stats_surface"], self.stats_ui_elements["best_stats_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_time_played_surface"], self.stats_ui_elements["total_time_played_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_rounds_played_surface"], self.stats_ui_elements["total_rounds_played_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_score_earned_surface"], self.stats_ui_elements["total_score_earned_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_shots_fired_surface"], self.stats_ui_elements["total_shots_fired_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_roids_destroyed_surface"], self.stats_ui_elements["total_roids_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_small_destroyed_surface"], self.stats_ui_elements["total_small_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_medium_destroyed_surface"], self.stats_ui_elements["total_medium_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["total_large_destroyed_surface"], self.stats_ui_elements["total_large_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["round_time_played_surface"], self.stats_ui_elements["round_time_played_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_score_surface"], self.stats_ui_elements["best_score_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_shot_chain"], self.stats_ui_elements["best_shot_chain_rect"])
            self.screen.blit(self.stats_ui_elements["best_roids_destroyed_surface"], self.stats_ui_elements["best_roids_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_small_destroyed_surface"], self.stats_ui_elements["best_small_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_medium_destroyed_surface"], self.stats_ui_elements["best_medium_destroyed_surface_rect"])
            self.screen.blit(self.stats_ui_elements["best_large_destroyed_surface"], self.stats_ui_elements["best_large_destroyed_surface_rect"])

        else:
            raise Exception(f"Invalid game_state: {self.game_state}")
       
        pygame.display.flip()