import difflib
import json
import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

from game import Game
from player import Player

# Get the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
players_path = os.path.join(BASE_DIR, "players.json")

# Load player data
with open(players_path, encoding="utf-8") as f:
    data = json.load(f)
players = [Player(**p) for p in data]

player_names = [player.name for player in players]
completer = FuzzyWordCompleter(player_names)

console = Console()

def print_header():
    console.print("\n[bold cyan]⚽ SUPER LIG WORDLE ⚽[/]\n", justify="center")

def find_guessed_player():
    while True:
        console.print("[bold cyan]🔍 Your guess: [/]")
        guess = prompt("", completer=completer).strip()
        
        # Exact or case-insensitive match
        for player in players:
            if player.name.lower() == guess.lower():
                console.clear()
                print_header()
                return player
        
        # Suggestion logic
        console.clear()
        print_header()
        matches = difflib.get_close_matches(guess, player_names, n=1, cutoff=0.6)
        if matches:
            console.print(f"[bold red]❌ Player not found.[/] Did you mean [bold cyan]'{matches[0]}'[/]?\n", justify="center")
        else:
            console.print("[bold red]❌ Player not found.[/] Please check the spelling or use the autocomplete.\n", justify="center")

def style_cell(cell):
    value = str(cell['value'])
    match cell["status"]:
        case "correct":
            return f"[bold green]{value}[/]"
        case "wrong":
            return f"[bold red]{value}[/]"
        case "group_match":
            return f"[bold yellow]{value}[/]"
        case "higher":
            return f"[bold yellow]{value} 📈[/]"
        case "lower":
            return f"[bold yellow]{value} 📉[/]"
    return value

def render_guesses(game):
    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("Name", justify="left")
    table.add_column("Age", justify="center")
    table.add_column("Nationality", justify="center")
    table.add_column("Club", justify="center")
    table.add_column("Position", justify="center")
    table.add_column("Number", justify="center")

    for rnd in game.rounds:
        table.add_row(
            style_cell(rnd["name"]),
            style_cell(rnd["age"]),
            style_cell(rnd["nationality"]),
            style_cell(rnd["club"]),
            style_cell(rnd["position"]),
            style_cell(rnd["number"])
        )

    round_num = len(game.rounds)
    panel = Panel(
        Align.center(table), 
        title=f"[bold white]Round {round_num}/{game.max_rounds}[/]", 
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(Align.center(panel))

def render_won_screen(guess, game):
    render_guesses(game)
    win_text = Text.from_markup(f"\n[bold green]🏆 CONGRATULATIONS! 🏆[/]\n\nYou guessed [bold cyan]{guess.name}[/] correctly!")
    console.print(Align.center(Panel(win_text, border_style="green", padding=(1, 2))))

def render_game_over_screen(game):
    loss_text = Text.from_markup(f"\n[bold red]💔 GAME OVER 💔[/]\n\nThe player was: [bold cyan]{game.target.name}[/]")
    console.print(Align.center(Panel(loss_text, border_style="red", padding=(1, 2))))

def main():
    while True:
        console.clear()
        print_header()
        game = Game(players, 10)
        
        last_guess = None
        while not game.is_over():
            if game.rounds:
                render_guesses(game)
            
            last_guess = find_guessed_player() 
            game.play_round(last_guess)
            
        if game.is_won():
            render_won_screen(last_guess, game)
        else:
            render_game_over_screen(game)
            
        while True:
            console.print("\n[bold yellow]🔄 Do you want to play again? (y/n): [/]", end="")
            choice = input().strip().lower()
            if choice == 'y':
                break
            elif choice == 'n':
                console.print("\n[bold cyan]Thanks for playing! Goodbye! 👋[/]\n", justify="center")
                sys.exit()
            else:
                console.print("[red]Invalid input. Please enter 'y' or 'n'.[/]")

if __name__ == "__main__":
    main()
