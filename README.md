# 🐍 Snake Game

## Description

**"Snake Game"** is a classic arcade game implemented in Python using the Pygame library.

The player controls a snake that moves across the game field, eating apples and growing in length. The goal is to grow the snake as long as possible while avoiding collisions with its own body.

<img width="628" height="507" alt="image" src="https://github.com/user-attachments/assets/f618b79e-6f07-42a1-9f5d-946d377816e6" />

---

## Project Features

1. **Game field:** 640x480 pixels, divided into 20x20 pixel cells.
2. **Controls:** WASD keys or arrow keys (↑, ↓, ←, →).
3. **Wall wrapping:** The snake reappears on the opposite side when moving out of the field boundaries.
4. **Game reset:** The snake resets to the initial state upon colliding with itself.
5. **Game speed:** 20 frames per second.

---

## Technologies

- Python 3.9+
- Pygame 2.0+

---

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/closecodex/the_snake
   cd the_snake

2. Install dependencies:
   ```bash
   pip install pygame
   
3. Run the game:
   ```bash
   python the_snake.py
