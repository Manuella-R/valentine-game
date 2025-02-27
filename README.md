# Cupid's Arrow - Pile Up Game

Cupid's Arrow is a simple yet addictive game where you shoot falling hearts before they pile up and reach your bow. The game is optimized for both PC and mobile devices, making it a fun experience on touchscreens.

## 🎮 Gameplay
- Hearts fall from the top of the screen.
- Tap anywhere to shoot an invisible arrow in that direction.
- If hearts reach the height of your bow, the game is over!
- Score points by hitting as many hearts as possible.

## 📦 Installation
### For Windows/Linux (Python)
1. Install Python 3.8 or later.
2. Install dependencies:
   ```sh
   pip install pygame
   ```
3. Run the game:
   ```sh
   python in.py
   ```

### For Android (APK Build)
1. Install **Buildozer**:
   ```sh
   pip install buildozer
   ```
2. Initialize Buildozer:
   ```sh
   buildozer init
   ```
3. Modify `buildozer.spec` file:
   - Set the package name, title, and permissions.
4. Build the APK:
   ```sh
   buildozer -v android debug
   ```
5. Transfer the APK from `bin/` to your phone and install it.

## 🎨 Customization
- Background image: Replace `background.jpg` with your own.
- Heart sprites: Add PNG images inside the `Red_Flowers` folder.
- Adjust game difficulty by changing heart spawn speed in the code.

## 🛠️ Requirements
- Python 3.8+
- Pygame
- Buildozer (for Android builds)

## 📜 License
This game is open-source and free to modify. Enjoy!

---
Happy gaming! 💘

