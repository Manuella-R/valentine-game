from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import random, os
import math

# Game settings
WIDTH, HEIGHT = Window.size
BOW_Y = HEIGHT * 0.3  # Bow position
HEARTS_FOLDER = "Red_Flowers"  # Folder with heart images

# Load heart images
heart_images = []
if os.path.exists(HEARTS_FOLDER):
    for filename in os.listdir(HEARTS_FOLDER):
        if filename.endswith(".png"):
            heart_images.append(os.path.join(HEARTS_FOLDER, filename))

# Game variables
score = 0
heart_spawn_timer = 0
SPAWN_INTERVAL = 30  # Lower = more hearts fall
game_over = False

class Heart(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = random.choice(heart_images)  # Pick a random heart image
        self.size = (30, 30)  # Set size for hearts
        self.x = random.randint(30, WIDTH - 30)
        self.y = -50
        self.speed = random.randint(1, 3)
        self.landed = False
        with self.canvas:
            self.heart_shape = Ellipse(pos=self.pos, size=self.size)

    def update(self, landed_hearts):
        if not self.landed:
            new_y = self.y + self.speed
            landing_surface = HEIGHT - self.height  # Bottom of screen

            for other in landed_hearts:
                if abs(self.x - other.x) < self.width:
                    candidate_surface = other.y - self.height
                    if candidate_surface < landing_surface:
                        landing_surface = candidate_surface

            if new_y >= landing_surface:
                self.y = landing_surface
                self.landed = True
            else:
                self.y = new_y
        self.heart_shape.pos = (self.x - self.width // 2, self.y - self.height // 2)

    def reset(self):
        self.image = random.choice(heart_images)
        self.x = random.randint(30, WIDTH - 30)
        self.y = -50
        self.speed = random.randint(2, 4)
        self.landed = False
        self.heart_shape.pos = (self.x - self.width // 2, self.y - self.height // 2)

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hearts = []
        self.landed_hearts = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = SPAWN_INTERVAL
        self.font = None  # For displaying text, we'll set it up later
        with self.canvas:
            self.bg = Rectangle(source="background.png", pos=self.pos, size=Window.size)
        Clock.schedule_interval(self.update, 1/60)

    def on_touch_down(self, touch):
        if not self.game_over:
            for heart in self.hearts:
                if (heart.x <= touch.x <= heart.x + heart.width) and (heart.y <= touch.y <= heart.y + heart.height):
                    self.score += 1
                    heart.reset()

    def update(self, dt):
        global game_over
        if self.game_over:
            return
        self.spawn_timer += 2
        if self.spawn_timer >= self.spawn_interval:
            heart = Heart()
            self.add_widget(heart)
            self.hearts.append(heart)
            self.spawn_timer = 0

        # Handle heart updates and landing
        landed_hearts = [heart for heart in self.hearts if heart.landed]
        for heart in self.hearts:
            heart.update(landed_hearts)

        for heart in self.hearts:
            if heart.landed and (heart.y - 15) <= HEIGHT // 2:
                self.game_over = True
                game_over = True
                print("Happy Valentines")

    def draw_score(self):
        # Create a font for displaying the score
        from kivy.core.text import Label
        label = Label(text=f"Score: {self.score}", font_size=36, pos=(10, HEIGHT - 40))
        self.add_widget(label)

    def draw_game_over(self):
        from kivy.core.text import Label
        label = Label(text="HAPPY VALENTINES <#", font_size=50, pos=(WIDTH // 2 - 160, HEIGHT // 2))
        self.add_widget(label)

    def on_draw(self):
        # Draw hearts and other elements
        for heart in self.hearts:
            heart.draw(self.canvas)

class CupidGameApp(App):
    def build(self):
        game = Game()
        return game

if __name__ == "__main__":
    CupidGameApp().run()
