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

    def render_guesses(game):
        for rnd in game.rounds:
            print(
                f"Name: {rnd['name']}, "
                f"Age: {rnd['age']}, " 
                f"Nationality: {rnd['nationality']}, "
                f"Club: {rnd['club']}, "
                f"Position: {rnd['position']}, "
                f"Number: {rnd['number']}"
            )
    def start_new_game():
        while True:
            print("Do you want to start a new game ? (y/n)")
            new_game = input()
            if new_game == "y":
                play()
            elif new_game == "n":
                sys.exit()
            else:
                print("Wrong entry.")

    def render_won_screen(guess):
        print(f"Congrats! Your player was {guess.name}")
        start_new_game()

    def render_game_over_screen(game):
        print(f"You ran out of guesses! Your player was {game.target.name}")
        start_new_game()

    def play():
        game = Game(players, 10)
        while not game.is_over():
            render_guesses(game) if game.rounds else None
            guess = find_guessed_player() 
            game.play_round(guess)
            render_won_screen(guess) if game.is_won() else None
        render_guesses(game)
        if game.is_over() and not game.is_won():
            render_game_over_screen(game)

    play()

main()


