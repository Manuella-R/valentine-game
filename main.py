import pygame, sys, math, random, os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupid's Arrow - Pile Up Game")
clock = pygame.time.Clock()

# Load background image
try:
    BG_IMAGE = pygame.image.load("download.jpg") 
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))
except:
    BG_IMAGE = pygame.Surface((WIDTH, HEIGHT))
    BG_IMAGE.fill((255, 200, 220))  # Pink fallback background

# Load heart images or create fallback hearts
HEARTS_FOLDER = "Red_Flowers"
heart_images = []

if os.path.exists(HEARTS_FOLDER):
    for img_file in os.listdir(HEARTS_FOLDER):
        if img_file.endswith(".png"):
            try:
                img = pygame.image.load(os.path.join(HEARTS_FOLDER, img_file))
                heart_images.append(pygame.transform.scale(img, (30, 30)))
            except:
                pass

# Create fallback heart if no images found
if not heart_images:
    fallback_heart = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(fallback_heart, (255, 0, 100), (10, 15), 8)
    pygame.draw.circle(fallback_heart, (255, 0, 100), (20, 15), 8)
    pygame.draw.polygon(fallback_heart, (255, 0, 100), [(5, 15), (25, 15), (15, 28)])
    heart_images.append(fallback_heart)  

class Heart:
    def __init__(self):
        self.image = random.choice(heart_images)
        self.x = random.randint(30, WIDTH - 30)
        self.y = -50
        self.speed = random.randint(1, 3)
        self.landed = False

    def update(self, landed_hearts):
        if not self.landed:
            new_y = self.y + self.speed
            landing_surface = HEIGHT - self.image.get_height()

            for other in landed_hearts:
                if abs(self.x - other.x) < self.image.get_width():
                    candidate_surface = other.y - self.image.get_height()
                    if candidate_surface < landing_surface:
                        landing_surface = candidate_surface

            if new_y >= landing_surface:
                self.y = landing_surface
                self.landed = True
            else:
                self.y = new_y

    def draw(self, surface):
        surface.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))

    def reset(self):
        self.image = random.choice(heart_images)
        self.x = random.randint(30, WIDTH - 30)
        self.y = -50
        self.speed = random.randint(2, 4)
        self.landed = False


hearts = []
score = 0
heart_spawn_timer = 0
SPAWN_INTERVAL = 30  # Adjusted for better laptop gameplay
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 48)
running = True
game_over = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Press R to restart when game is over
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            hearts = []
            score = 0
            heart_spawn_timer = 0
            game_over = False

        # Mouse click to hit hearts (laptop-friendly)
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for heart in hearts:
                if math.hypot(mx - heart.x, my - heart.y) < 15:
                    score += 1
                    heart.reset()
                    break  # Only hit one heart per click

    if not game_over:
        heart_spawn_timer += 2
        if heart_spawn_timer >= SPAWN_INTERVAL:
            hearts.append(Heart())
            heart_spawn_timer = 0

        landed_hearts = [heart for heart in hearts if heart.landed]
        for heart in hearts:
            heart.update(landed_hearts)

        for heart in hearts:
            if heart.landed and (heart.y - 15) <= HEIGHT // 2:
                game_over = True
                break

    screen.blit(BG_IMAGE, (0, 0))

    for heart in hearts:
        heart.draw(screen)

    score_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    # Display game over screen with restart instructions
    if game_over:
        game_over_surface = title_font.render("GAME OVER", True, (255, 0, 0))
        restart_surface = font.render("Press R to Restart", True, (0, 0, 0))
        final_score_surface = font.render(f"Final Score: {score}", True, (0, 0, 0))
        
        screen.blit(game_over_surface, ((WIDTH - game_over_surface.get_width()) // 2, HEIGHT // 2 - 40))
        screen.blit(final_score_surface, ((WIDTH - final_score_surface.get_width()) // 2, HEIGHT // 2 + 10))
        screen.blit(restart_surface, ((WIDTH - restart_surface.get_width()) // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
