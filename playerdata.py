import json
import os
from datetime import datetime
from constants import SIZE_SMALL, SIZE_MEDIUM, SIZE_LARGE

class PlayerData:
    def __init__(self):
        self.total_time_played = 0.0 # seconds
        self.total_rounds_played = 0
        self.total_score_earned = 0

        self.total_asteroids_destroyed = 0
        self.asteroids_destroyed_by_size = {SIZE_SMALL: 0, SIZE_MEDIUM: 0, SIZE_LARGE: 0}
        self.total_shots_fired = 0

        self.longest_round = 0.0 # seconds
        self.highest_single_round_score = 0
        self.longest_consecutive_shot_chain = 0
        self.most_asteroids_destroyed_single_round = 0
        self.most_asteroids_destroyed_by_size_single_round = {}

    @classmethod
    def load_data(cls, filepath):
        if not os.path.exists(filepath):
            print(f"No player data file exists at {filepath}. Creating new player data.")
            return cls()

        try:
            with open(filepath, 'r') as f:
                loaded_dict = json.load(f)
            
            player_data = cls()

            for key, value in loaded_dict.items():
                if hasattr(player_data, key):
                    setattr(player_data, key, value)
                else:
                    print(f"Warning: Attribute '{key}' from save file not found in current PlayerData class. Ignoring.")
                
            print(f"Player data loaded successfully from {filepath}.")
            return player_data
        
        except json.JSONDecodeError:
            print(f"Error: Player data file at {filepath} is corrupted. Creating new player data.")
            return cls()
        
        except Exception as e:
            print(f"An unexpected error occurred while loading player data: {e}. Creating new player data.")
            return cls()
    
    def save_data(self, filepath):
        try:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, 'w') as f:
                json.dump(self.__dict__, f, indent=4)
            
            print(f"Player data saved successfully to {filepath}.")

        except Exception as e:
            print(f"An error occurred while saving player data to {filepath}: {e}")

    def collect_and_record_round_data(self, round):
        self.total_time_played += round.round_time
        self.total_rounds_played += 1
        self.total_score_earned += round.round_score
        self.total_asteroids_destroyed += round.round_asteroids_destroyed
        
        for key in round.round_asteroids_destroyed_by_size:
            if key not in self.asteroids_destroyed_by_size:
                self.asteroids_destroyed_by_size[key] = 0
            self.asteroids_destroyed_by_size[key] += round.round_asteroids_destroyed_by_size[key]
        
        self.total_shots_fired += round.round_shots_fired

        if round.round_time > self.longest_round:
            self.longest_round = round.round_time
        
        if round.round_score > self.highest_single_round_score:
            self.highest_single_round_score = round.round_score
        
        if round.longest_consecutive_shot_chain > self.longest_consecutive_shot_chain:
            self.longest_consecutive_shot_chain = round.longest_consecutive_shot_chain
        
        if round.round_asteroids_destroyed > self.most_asteroids_destroyed_single_round:
            self.most_asteroids_destroyed_single_round = round.round_asteroids_destroyed
            self.most_asteroids_destroyed_by_size_single_round.clear()
            self.most_asteroids_destroyed_by_size_single_round = round.round_asteroids_destroyed_by_size


