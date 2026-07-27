# Super Lig Wordle 

A terminal-based Wordle clone for the Turkish Süper Lig — guess the mystery player in 10 tries!

Each guess is scored against the target player across attributes like position, age, and shirt number, so you narrow the field down clue by clue, just like Wordle.

## Requirements

- Python 3
- pip

## Getting Started

### 1. Installation

Install the required dependencies:

```bash
./setup.sh
```

This installs `rich`, `prompt_toolkit`, `requests`, `beautifulsoup4`, and `python-dotenv`.

### 2. Run the Game

To start the game, simply run:

```bash
./run.sh
```

## How to Play

- You have **10 rounds** to guess the target player.
- Use **autocomplete** (tab or arrow keys) to find player names as you type.
- After each guess, a table shows how close you are:
  - 🟩 **Green** — Correct!
  - 🟥 **Red** — Wrong.
  - 🟨 **Yellow (Position)** — Correct position group (e.g., you guessed LW, the target is RW — both are forwards).
  - 📈 / 📉 **Arrows (Age/Number)** — Shows whether the target's value is higher or lower than your guess.

## Updating Player Data

The game includes a built-in web scraper that pulls the **Top 50 most valued players** directly from Transfermarkt. To refresh the database with current stats:

```bash
python3 src/update_players.py
```

## Project Structure

```
.
├── run.sh                  # Launches the game
├── setup.sh                # Installs Python dependencies
└── src/
    ├── main.py              # Entry point and UI logic
    ├── game.py               # Core game engine
    ├── round.py              # Guess comparison and evaluation logic
    ├── update_players.py     # Transfermarkt web scraper
    └── players.json           # Player database
```

## Data Source

Player data is scraped from [Transfermarkt](https://www.transfermarkt.com/). Since values and squads change over time, re-run the scraper periodically to keep the database current.

## License

No license has been specified for this project yet.
