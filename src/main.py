from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from game import Game
from player import Player
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

def main():
    with open("src/players.json") as f:
        data = json.load(f)
    players = [Player(**p) for p in data]

    player_names = []
    for player in players:
        player_names.append(player.name)
    completer = FuzzyWordCompleter(player_names)

    console = Console()

    def find_guessed_player():
        console.print("[bold cyan]🔍 Your guess: [/]")
        guess = prompt("", completer=completer)
        console.clear()
        console.print("\n[bold cyan]⚽ SUPER LIG WORDLE ⚽[/]\n", justify="center")
        for player in players:
            if player.name == guess:
                return player
        print("You typed a wrong player! Please guess again.")
        return find_guessed_player()

    def style_cell(cell, arrows = False):
        match cell["status"]:
            case "correct":
                return f"[green]{cell['value']}[/]"
            case "wrong":
                return f"[red]{cell['value']}[/]"
            case "group_match":
                return f"[yellow]{cell['value']}[/]"
            case "higher":
                return f"[yellow]{cell['value']} 📈[/]"
            case "lower":
                return f"[yellow]{cell['value']} 📉[/]"

    def render_guesses(game):
        table = Table(title="Your Guesses")
        table.add_column("Name")
        table.add_column("Age")
        table.add_column("Nationality")
        table.add_column("Club")
        table.add_column("Position")
        table.add_column("Number")

        for rnd in game.rounds:
            name_cell = rnd["name"]
            age_cell = rnd["age"]
            nation_cell = rnd["nationality"]
            club_cell = rnd["club"]
            pos_cell = rnd["position"]
            num_cell = rnd["number"]
            
            table.add_row(
                style_cell(name_cell),
                style_cell(age_cell, arrows = True),
                style_cell(nation_cell),
                style_cell(club_cell),
                style_cell(pos_cell),
                style_cell(num_cell, arrows = True)
            )

        round_num = len(game.rounds)
        panel = Panel(table, title=f"Round {round_num}/{game.max_rounds}", border_style="bright_blue")
        console.print(Align.center(panel))
    
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

    def render_won_screen(guess,game):
        render_guesses(game)
        console.print(Align.center(Panel(f"[bold green]🎉 CONGRATS! You guessed {guess.name}! 🎉[/]", border_style="green")))
        start_new_game()

    def render_game_over_screen(game):
        console.print(Align.center(Panel(f"[bold red]😔 GAME OVER![/] [yellow]The player was:[/] [bold cyan]{game.target.name}[/]", border_style="red")))
        start_new_game()

    def play():
        console.clear()
        console.print("\n[bold cyan]⚽ SUPER LIG WORDLE ⚽[/]\n", justify="center")
        game = Game(players, 10)
        while not game.is_over():
            render_guesses(game) if game.rounds else None
            guess = find_guessed_player() 
            game.play_round(guess)
            render_won_screen(guess, game) if game.is_won() else None 
        if game.is_over() and not game.is_won():
            render_game_over_screen(game)

    play()

main()


