# tic-tac-toe
AI driven Tic Tac Toe in CoppeliaSim
# 🤖 Tic Tac Toe with CoppeliaSim + Python GUI

This project is an interactive **Tic Tac Toe game** built with **Python (Tkinter GUI)** and integrated with **CoppeliaSim** to control physical token placement on a virtual board.

It includes three gameplay modes:

- 🧑 **Manual Mode** – Two-player mode with name prompts
- 🧠 **Basic AI Mode** – Human vs AI (simple logic)
- 🧠💡 **Minimax AI Mode** – Human vs AI using unbeatable Minimax algorithm

---

## 🎮 Features

- 🎛️ GUI built in **Tkinter**
- 🔊 **Voice prompts** using `pyttsx3` (cross-platform)
- 🎥 **CoppeliaSim integration** for visual token placement
- 🧠 Smart AI options: Basic or Minimax
- 🔁 **Replayable game sessions**
- 🎉 Announces win or draw by name and voice

---

## 🖥️ Requirements

- Python 3.x
- CoppeliaSim (with ZMQ Remote API enabled)
- Required Python libraries:
  ```bash
  pip install pyttsx3
  pip install coppeliasim_zmqremoteapi_client

🧩 How It Works

    The GUI board is numbered 0–8:

     0 | 1 | 2
    -----------
     3 | 4 | 5
    -----------
     6 | 7 | 8

    Token pieces (token_X_0 to token_X_4, token_O_0 to token_O_4) are moved using Python code in sync with GUI moves.

🛠️ Getting Started

    Open tictactoe_gui_final.py in your Python IDE or terminal

    Start CoppeliaSim and load your tictactoe.ttt scene

    Run the script:

    python tictactoe_gui_final.py

    Select a mode (Manual, Basic AI, or Minimax AI)

    Play and enjoy the interactive experience!

📷 Screenshots

    Add screenshots showing the GUI and CoppeliaSim board here

📚 Educational Use

This project was designed for a library “show and tell” session to teach kids and adults about:

    Human-computer interaction

    AI algorithms

    Robotics integration via simulation

📦 Folder Structure

.
├── tictactoe_gui_final.py        # Main application
├── tictactoe.ttt                 # CoppeliaSim scene (drag & drop tokens)
└── README.md                     # You're here!

📜 License

MIT License – open for educational and public showcase use.
🙌 Author

Created by Daniel Christadoss using collaborative ai.
