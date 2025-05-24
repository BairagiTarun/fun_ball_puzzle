# 🎮 Fun Ball Puzzle

A colorful and fun ball-catching puzzle game made with **Python** and **Pygame**.

In this arcade-style game, you control a paddle to catch falling balls of various sizes and colors. The smaller the ball, the more points you get. Avoid missing too many balls — or the screen will overflow, ending the game early!

> 🛠 **Built using [Amazon Q Developer CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is-qdeveloper.html)**
> Amazon Q CLI lets you generate, refactor, and document code using natural language prompts — directly in your terminal or code editor.

---

## 🚀 Powered by Amazon Q CLI

This game was created using the **Amazon Q CLI**, a powerful tool that helps developers:

* ⚡ **Generate complete applications** from simple prompts
* 🛠️ **Refactor and fix bugs** in your existing code
* 📚 **Add documentation and comments** to your codebase
* 🔍 **Search and navigate codebases** using AI
* 🧠 **Understand code behavior** with natural language queries

### 🧾 Prompt Used

```
Create a simple Fun Ball Puzzle game using Python and Pygame. The game should have the following features:

1. A window with a colorful background.
2. Multiple balls of different colors moving randomly on the screen.
3. The player controls a paddle or a catcher at the bottom of the screen using left and right arrow keys.
4. The goal is to catch the balls with the paddle to score points.
5. Each caught ball adds points; missed balls don’t count.
6. The game runs with smooth animation and simple sound effects for catching balls.
7. Display the score at the top of the screen.
8. Include a start screen with instructions and a game over screen showing the final score.
9. Use clear and readable fonts.
10. The code should be modular and well-commented.

Use Pygame library to implement the game.
```

---

## 🖼 Features

* 🎨 Colorful animated background
* 🟡 Balls of varying sizes and random colors
* 🕹️ Paddle movement via arrow keys
* 🎯 Score points by catching balls
* 🧠 Smaller balls = more points
* ⏱️ 60-second game timer
* 🔊 Catch sound effects
* 📺 Start screen with instructions
* 💀 Game over screen with score and replay option
* 📚 Clean, modular, well-commented code

---

## 📷 Screenshots

*(You can add images of the Start Screen, Gameplay, and Game Over Screen here.)*

---

## 🧩 Game Structure

```
fun_ball_puzzle/
├── fun_ball_puzzle.py     # Main game script
├── sounds/
│   └── catch.wav          # Sound effect for catching balls
└── README.md              # Project documentation
```

---

## 🧠 Gameplay Overview

* Use `LEFT` and `RIGHT` arrow keys to move the paddle.
* Catch the falling balls — smaller balls score higher!
* Avoid letting too many balls fall.
* Game ends when:

  * ⏲️ Time runs out
  * 🔴 More than 20 balls are on screen at once
* Simple sound feedback when balls are caught.

---

## 🔧 Requirements

* Python 3.x
* [`pygame`](https://www.pygame.org/news)

Install pygame using:

```bash
pip install pygame
```

---

## ▶️ How to Play

```bash
python fun_ball_puzzle.py
```

### Controls:

| Key      | Action               |
| -------- | -------------------- |
| ⬅️ Left  | Move paddle left     |
| ➡️ Right | Move paddle right    |
| Spacebar | Start / Restart game |
| ESC      | Quit the game        |

---

## 👨‍💻 Author

Created by **Tarun Bairagi**
Developed with 💡 **Amazon Q Developer CLI** and ❤️ **Pygame**

---

## 🧰 Want to Try Amazon Q CLI?

1. Install the Amazon Q Developer CLI:
   [Installation Guide →](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/qdeveloper-install.html)

2. Authenticate with your AWS account.

3. Start building by typing prompts like:

   ```
   qdev codegen "Create a ball-catching game using Pygame"
   ```

4. Watch Amazon Q generate real, runnable code ✨

---
