from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from game import Game
from player import Player
import json
import sys


def main():
    with open("src/players.json") as f:
        data = json.load(f)
    players = [Player(**p) for p in data]
    player_names = []
    for player in players:
        player_names.append(player.name)
    completer = FuzzyWordCompleter(player_names)
    def find_guessed_player():
        guess = prompt("Guess: ", completer=completer)
        for player in players:
            if player.name == guess:
                return player
        print("You typed a wrong player! Please guess again.")
        return find_guessed_player()
                
    
    def start_game():
        game = Game(players, 10)
        while not game.is_over():
            if game.rounds:
                for round in game.rounds:
                    print(f"Name: {round['name']}, Age: {round['age']}, Nationality: {round['nationality']}, Club: {round['club']}, Position: {round['position']}, Number: {round['number']}")
            guess = find_guessed_player()
            if guess.name == game.target.name:
                print(f"Congrats! Your player was {guess.name}")
                while True:
                    print("Do you want to start a new game ? (y/n)")
                    new_game = input()
                    if new_game == "y":
                        start_game()
                    elif new_game == "n":
                        sys.exit()
                    else:
                        print("Wrong entry.")

            
            game.play_round(guess)


    start_game()


        

    
    

main()


