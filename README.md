# Cupid's Arrow - Pile Up Game 💘

An addictive arcade game where you click to hit falling hearts before they pile up! Featuring combo systems, power-ups, particle effects, and progressive difficulty. Designed for desktop/laptop gameplay!

## ✨ Features

### 🎮 Core Gameplay
- **Hearts Stack Dynamically**: Hearts fall and pile up on each other realistically
- **3 Lives System**: Get multiple chances before game over
- **Progressive Difficulty**: Game gets harder as you level up (20 hearts per level)
- **Bonus Golden Hearts**: Rare golden hearts worth 10x points with sparkle effects!
- **High Score Tracking**: Beat your personal best!

### 🎯 Combo System
- Build combos by hitting hearts in quick succession
- Combo multiplier up to **x10**!
- 2-second window to maintain combos
- Animated combo display with pulsing effects

### 💥 Power-Ups (10% drop chance)
- **🔵 Slow-Mo (S)**: Slows down all hearts for 3 seconds
- **🔴 Bomb (B)**: Clears all falling hearts instantly
- **🟢 Shield (H)**: Protects you from game over for 5 seconds

### 🌟 Visual Effects
- **Particle explosions** when hearts are hit (pink for regular, gold for bonus)
- **Floating score popups** showing points earned
- **Shadows and outlines** on all hearts for better visibility
- **Pulsing danger line** warning when hearts get too high
- **Glowing power-ups** with animated effects
- **Text outlines** for perfect readability on any background

### 🎨 Enhanced UI
- Score counter with high score display
- Lives shown as heart icons
- Current level indicator
- Active power-up timers
- Animated combo display
- Pause screen overlay
- Detailed game over screen

## 🖱️ Controls

| Key/Action | Function |
|------------|----------|
| **Mouse Click** | Click on hearts to hit them |
| **SPACE or P** | Pause/Unpause the game |
| **R** | Restart after game over |
| **Move Mouse** | Collect power-ups by hovering over them |

## 📦 Installation

### For Windows/Linux/Mac
1. Install Python 3.8 or later
2. Install Pygame:
   ```sh
   pip install pygame
   ```
3. Run the game:
   ```sh
   python main.py
   ```
   Or alternatively:
   ```sh
   python in.py
   ```

## 🎯 Gameplay Tips

- **Build Combos**: Hit hearts quickly in succession for massive score multipliers
- **Prioritize Golden Hearts**: They're worth 10x points!
- **Use Power-Ups Wisely**: Save slow-mo and shields for when hearts pile up dangerously
- **Watch the Danger Line**: The pulsing red line shows when hearts are getting too high
- **Level Up**: Every 20 hearts hit increases difficulty but also shows your skill!

## 🏆 Scoring System

- Regular heart: **1 point** (×combo multiplier)
- Golden heart: **10 points** (×combo multiplier)
- Combo multiplier: Up to **10x**
- Example: Golden heart at 5x combo = **50 points**!

## 🎨 Customization

- **Background image**: Replace `download.jpg` with your own 800×600 image
- **Heart sprites**: Add PNG images inside the `Red_Flowers` folder
- **Game difficulty**: Adjust `SPAWN_INTERVAL` in code (default: 30, lower = harder)
- **Window size**: Modify `WIDTH` and `HEIGHT` variables
- **Lives**: Change `self.lives = 3` to any number you want
- **Power-up chances**: Adjust `random.random() < 0.1` for power-up drop rate

## 🛠️ Requirements

- Python 3.8+
- Pygame library
- Works on Windows, Linux, and Mac!

## 🎪 Game Mechanics

### Difficulty Progression
- Starts at Level 1 with moderate speed
- Every 20 hearts hit = level up
- Spawn interval decreases by 2 frames per level
- Minimum spawn interval: 15 frames (maximum difficulty)

### Lives System
- Start with 3 lives
- Lose a life when hearts reach the danger line
- Game clears some hearts after losing a life (gives you a chance!)
- Shield power-up can save you from losing a life

## 📜 License

This game is open-source and free to modify. Enjoy!

---

**Happy gaming!** 💘 Can you reach Level 10?

