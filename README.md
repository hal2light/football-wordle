# ⚽ Super Lig Wordle ⚽

A terminal-based Wordle clone for the Turkish Süper Lig. Guess the mystery player in 10 tries!

## 🚀 Getting Started

### 1. Installation
First, install the required dependencies:
```bash
./setup.sh
```

### 2. Run the Game
To start the game, simply run:
```bash
./run.sh
```

## 🎮 How to Play
- You have **10 rounds** to guess the target player.
- Use the **Autocomplete** (tab or arrow keys) to find player names.
- After each guess, the table will show how close you are:
    - 🟩 **Green**: Correct!
    - 🟥 **Red**: Wrong.
    - 🟨 **Yellow (Position)**: Correct Position Group (e.g., guessed LW, target is RW - both are Forwards).
    - 📈/📉 **Arrows (Age/Number)**: Indicates if the target's value is higher or lower than your guess.

## 🔄 Updating Player Data
The game includes a built-in web scraper that pulls the **Top 50 most valued players** directly from Transfermarkt. To update the database with fresh stats:
```bash
python3 src/update_players.py
```

## 🛠️ Project Structure
- `src/main.py`: The entry point and UI logic.
- `src/game.py`: Core game engine.
- `src/round.py`: Comparison and evaluation logic.
- `src/update_players.py`: Transfermarkt web scraper.
- `src/players.json`: The player database.
