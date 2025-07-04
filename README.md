# 🟩 Terminal Tetris Game in Python 🎮

A classic **Tetris game** built with Python that runs directly in your **terminal** using `curses`.  
Inspired by the aesthetic from the *Tetris movie*, using `[]` blocks and a green-colored border.

---

## 📦 Features

- ⬜ Terminal-based interface (no GUI/pygame)
- 🎮 Arrow-key controls for gameplay
- 🧱 Tetris pieces (`I`, `O`, `T`, `S`, `Z`, `J`, `L`) with rotation
- 🟩 Green-colored borders and clean ASCII grid
- 💥 Line clearing with scoring system
- ✅ Written in clean, beginner-friendly Python code

---

## 🎮 Controls

| Key         | Action         |
|-------------|----------------|
| ⬅️ Left arrow  | Move left     |
| ➡️ Right arrow | Move right    |
| ⬇️ Down arrow  | Soft drop     |
| ⬆️ Up arrow    | Rotate piece |
| `Q` or `q`    | Quit game     |

---

## ▶️ Run the Game

### 💻 Requirements
- Python 3.6+
- Unix-based terminal (Linux/macOS) or Windows with compatible terminal (e.g., WSL, Git Bash)

### 🛠 Installation

```bash
git clone https://github.com/shadow-031/tetria
cd tetris
python3 tetris.py
