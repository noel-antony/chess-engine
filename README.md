# Python Chess Engine

A fully functional, custom-built chess engine and graphical user interface (GUI) written entirely in Python. This project was developed from scratch as a B.Tech microproject and features a sophisticated move generator, an optimized AI, and a modern, polished desktop interface.

## Features

### 🧠 Custom AI Engine (`engine/`)
- **Minimax Algorithm**: Evaluates thousands of potential board states to find the best move.
- **Alpha-Beta Pruning**: Drastically reduces the number of nodes evaluated in the search tree.
- **Move Ordering**: Utilizes MVV-LVA (Most Valuable Victim - Least Valuable Attacker) to maximize Alpha-Beta cutoffs.
- **Quiescence Search**: Extends search paths during tactical exchanges to prevent the "horizon effect".
- **Evaluation Function**: Highly tuned piece-square tables and material evaluations for positional understanding.

### ♟️ Chess Logic (`chess/`)
- **Move Generation**: Fully compliant with all FIDE chess rules.
- **Special Moves**: Native support for Castling, En Passant, and Pawn Promotion.
- **Validation**: Strict Perft (Performance Test) validation against standard move generation counts.

### 🎨 Modern GUI (`ui/`)
- **Custom Theming**: Sleek dark mode aesthetics with responsive hover effects.
- **Dynamic Highlights**: Highlights last moves, selected squares, and legal move destinations.
- **Real-time Evaluation Bar**: Visually displays the engine's assessment of the current position.
- **Move History & Material Tracking**: Logs Algebraic-like notation and elegantly displays captured material via SVGs.
- **Asynchronous AI**: Background threading ensures the GUI remains perfectly fluid while the engine calculates.

## Project Structure

- `chess/`: Core chess logic.
  - `board.py`: Manages the board state, making/undoing moves, and castling/en-passant rights.
  - `move_generator.py`: Generates pseudo-legal moves and identifies attacks/checks.
  - `piece.py`, `move.py`: Data structures representing pieces and moves.
- `engine/`: AI and evaluation logic.
  - `minimax.py`: The core search algorithm using Alpha-Beta pruning, MVV-LVA move ordering, and Quiescence search.
  - `evaluation.py`: Static evaluation logic including material advantage and piece-square tables.
  - `agent.py`: High-level interface to connect the engine with the game state.
- `ui/`: Graphical User Interface powered by `PySide6`.
  - `main_window.py`: The entry point for the desktop window, managing overall layout.
  - `chess_board.py`: Renders the board and pieces (using SVGs from `assets/`) and handles user interactions.
  - `ai_worker.py`: Runs the engine calculations on a background `QThread` to prevent UI freezing.
  - Additional components include `evaluation_bar.py`, `game_panel.py`, `move_history.py`, and custom dialogs for promotion and game-over states.
- `tests/`: Automated test suite.
  - Includes tests for move generation, engine evaluation, captures, state transitions, and strict Perft validations.
- `main.py`: The main entry point script to run the application.
- `Chess_Engine_Demo.ipynb`: A Jupyter Notebook demonstrating the underlying mechanics of board state and move generation in an isolated environment.

## Installation & Setup

1. **Clone the repository.**
2. **Install dependencies:**
   This project uses `PySide6` for the user interface. Ensure you have Python 3.8+ installed.
   ```bash
   pip install PySide6
   ```
3. **Run the Application:**
   ```bash
   python main.py
   ```

## Running the Automated Tests

The engine includes an automated integration testing suite to verify board states, checkmate detection, en passant, and the Minimax solver.
To run the tests from the root directory:
```bash
python -m unittest discover -s tests
```
*Note: You can also run specific test files directly, for example:*
```bash
python -m tests.test_engine
```

## Demonstration

A Jupyter Notebook (`Chess_Engine_Demo.ipynb`) is provided for presentation purposes. It walks through the internal representations of the board, demonstrates move generation, and benchmarks the AI in isolated scenarios.
