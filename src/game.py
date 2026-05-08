import random
from player import Player
from round import Round

class Game:
    def __init__(self, players, max_rounds = 10):
        self.target = random.choice(players)
        self.rounds = []
        self.max_rounds = max_rounds
    
    def play_round(self, guess_player):
        r = Round(guess_player, self.target)
        result = r.evaluate()
        self.rounds.append(result)
        return result
    
    def is_won(self):
        return self.rounds and self.rounds[-1]["name"]["value"] == self.target.name

    def is_over(self):
        return self.is_won() or len(self.rounds) >= self.max_rounds

            


