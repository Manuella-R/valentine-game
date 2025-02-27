import pygame, sys, math, random, os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupid's Arrow - Pile Up Game")
clock = pygame.time.Clock()


BG_IMAGE = pygame.image.load("download.jpg") 
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))  


HEARTS_FOLDER = "Red_Flowers"
heart_images = [pygame.image.load(os.path.join(HEARTS_FOLDER, img)) for img in os.listdir(HEARTS_FOLDER) if img.endswith(".png")]
heart_images = [pygame.transform.scale(img, (30, 30)) for img in heart_images]  

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


hearts = [Heart() for _ in range(15)]
score = 0
heart_spawn_timer = 0
SPAWN_INTERVAL = 20
font = pygame.font.SysFont(None, 36)
running = True
game_over = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for heart in hearts:
                if math.hypot(mx - heart.x, my - heart.y) < 15:
                    score += 1
                    heart.reset()

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

    if game_over:
        game_over_surface = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(game_over_surface, ((WIDTH - game_over_surface.get_width()) // 2, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
