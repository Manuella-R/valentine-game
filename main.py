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
                heart_images.append(pygame.transform.scale(img, (35, 35)))
            except:
                pass

# Create fallback hearts with different colors
if not heart_images:
    # Regular heart (red)
    regular_heart = pygame.Surface((35, 35), pygame.SRCALPHA)
    pygame.draw.circle(regular_heart, (255, 0, 100), (12, 17), 9)
    pygame.draw.circle(regular_heart, (255, 0, 100), (23, 17), 9)
    pygame.draw.polygon(regular_heart, (255, 0, 100), [(6, 17), (29, 17), (17.5, 32)])
    # Add white outline for visibility
    pygame.draw.circle(regular_heart, (255, 255, 255), (12, 17), 9, 2)
    pygame.draw.circle(regular_heart, (255, 255, 255), (23, 17), 9, 2)
    pygame.draw.polygon(regular_heart, (255, 255, 255), [(6, 17), (29, 17), (17.5, 32)], 2)
    heart_images.append(regular_heart)
    
    # Golden heart (bonus)
    golden_heart = pygame.Surface((35, 35), pygame.SRCALPHA)
    pygame.draw.circle(golden_heart, (255, 215, 0), (12, 17), 9)
    pygame.draw.circle(golden_heart, (255, 215, 0), (23, 17), 9)
    pygame.draw.polygon(golden_heart, (255, 215, 0), [(6, 17), (29, 17), (17.5, 32)])
    pygame.draw.circle(golden_heart, (255, 255, 255), (12, 17), 9, 2)
    pygame.draw.circle(golden_heart, (255, 255, 255), (23, 17), 9, 2)
    pygame.draw.polygon(golden_heart, (255, 255, 255), [(6, 17), (29, 17), (17.5, 32)], 2)
    heart_images.append(golden_heart)

# Particle effect class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.lifetime = 30
        self.color = color
        self.size = random.randint(3, 6)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # gravity
        self.lifetime -= 1
        self.size = max(1, self.size - 0.1)
    
    def draw(self, surface):
        alpha = int((self.lifetime / 30) * 255)
        color_with_alpha = (*self.color[:3], alpha)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
        surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

# Score popup class
class ScorePopup:
    def __init__(self, x, y, score, combo=1):
        self.x = x
        self.y = y
        self.score = score
        self.combo = combo
        self.lifetime = 40
        self.vy = -2
        
    def update(self):
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface, font):
        alpha = int((self.lifetime / 40) * 255)
        text = f"+{self.score}"
        if self.combo > 1:
            text = f"+{self.score} x{self.combo}!"
            color = (255, 200, 0)
        else:
            color = (255, 255, 255)
        
        # Create text with outline for visibility
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, (0, 0, 0))
        
        # Draw outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            surface.blit(outline_surface, (int(self.x + dx), int(self.y + dy)))
        surface.blit(text_surface, (int(self.x), int(self.y)))

# Power-up class
class PowerUp:
    def __init__(self, x, y, type_name):
        self.x = x
        self.y = y
        self.type = type_name
        self.speed = 2
        self.size = 25
        self.lifetime = 180  # 3 seconds
        self.colors = {
            'slowmo': (100, 200, 255),
            'bomb': (255, 100, 100),
            'shield': (100, 255, 100)
        }
        
    def update(self):
        self.y += self.speed
        self.lifetime -= 1
        
    def draw(self, surface, font):
        color = self.colors.get(self.type, (255, 255, 255))
        # Draw with pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 5
        size = self.size + pulse
        
        # Draw glow
        glow_surface = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, 50), (size * 1.5, size * 1.5), size * 1.5)
        surface.blit(glow_surface, (self.x - size * 1.5, self.y - size * 1.5))
        
        # Draw power-up
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(size))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(size), 2)
        
        # Draw icon
        icon_font = pygame.font.SysFont(None, 20)
        icons = {'slowmo': 'S', 'bomb': 'B', 'shield': 'H'}
        icon_text = icon_font.render(icons.get(self.type, '?'), True, (0, 0, 0))
        surface.blit(icon_text, (self.x - icon_text.get_width() // 2, self.y - icon_text.get_height() // 2))

class Heart:
    def __init__(self):
        self.image = random.choice(heart_images)
        self.x = random.randint(40, WIDTH - 40)
        self.y = -50
        self.speed = random.randint(1, 3)
        self.landed = False
        # Bonus hearts are rarer and worth more
        self.is_bonus = random.random() < 0.15  # 15% chance
        if self.is_bonus and len(heart_images) > 1:
            self.image = heart_images[1]  # Golden heart
        self.size = self.image.get_width()

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
        # Add shadow for better visibility
        shadow = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        surface.blit(shadow, (self.x - self.size // 2 + 2, self.y - self.size // 2 + 2))
        
        # Draw heart
        surface.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
        
        # Bonus hearts have sparkle effect
        if self.is_bonus:
            sparkle_offset = math.sin(pygame.time.get_ticks() * 0.01) * 3
            sparkle_color = (255, 255, 200, 150)
            s = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(s, sparkle_color, (4, 4), 3)
            surface.blit(s, (self.x - 4, self.y - self.size // 2 + sparkle_offset))

    def reset(self):
        self.image = random.choice(heart_images)
        self.x = random.randint(40, WIDTH - 40)
        self.y = -50
        self.speed = random.randint(2, 4)
        self.landed = False
        self.is_bonus = random.random() < 0.15
        if self.is_bonus and len(heart_images) > 1:
            self.image = heart_images[1]

# Game state
class GameState:
    def __init__(self):
        self.hearts = []
        self.particles = []
        self.score_popups = []
        self.powerups = []
        self.score = 0
        self.high_score = 0
        self.combo = 0
        self.combo_timer = 0
        self.game_over = False
        self.paused = False
        self.spawn_timer = 0
        self.spawn_interval = 30
        self.level = 1
        self.hearts_hit = 0
        self.lives = 3
        self.slowmo_timer = 0
        self.shield_timer = 0
        self.game_speed = 1.0
        
    def reset(self):
        self.hearts = []
        self.particles = []
        self.score_popups = []
        self.powerups = []
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.game_over = False
        self.paused = False
        self.spawn_timer = 0
        self.spawn_interval = 30
        self.level = 1
        self.hearts_hit = 0
        self.lives = 3
        self.slowmo_timer = 0
        self.shield_timer = 0
        self.game_speed = 1.0

game_state = GameState()
font = pygame.font.SysFont(None, 32)
title_font = pygame.font.SysFont(None, 56)
small_font = pygame.font.SysFont(None, 24)
running = True

# Main game loop
while running:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Press R to restart when game is over
            if game_state.game_over and event.key == pygame.K_r:
                if game_state.score > game_state.high_score:
                    game_state.high_score = game_state.score
                game_state.reset()
            
            # Press P or SPACE to pause
            if not game_state.game_over and event.key in [pygame.K_p, pygame.K_SPACE]:
                game_state.paused = not game_state.paused

        # Mouse click to hit hearts (laptop-friendly)
        if not game_state.game_over and not game_state.paused and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            hit_heart = None
            
            for heart in game_state.hearts:
                if math.hypot(mx - heart.x, my - heart.y) < 18:
                    hit_heart = heart
                    break
            
            if hit_heart:
                # Score calculation
                base_score = 10 if hit_heart.is_bonus else 1
                game_state.combo += 1
                game_state.combo_timer = 120  # 2 seconds to maintain combo
                
                combo_multiplier = min(game_state.combo, 10)
                points = base_score * combo_multiplier
                game_state.score += points
                game_state.hearts_hit += 1
                
                # Create particles
                particle_color = (255, 215, 0) if hit_heart.is_bonus else (255, 100, 150)
                for _ in range(10):
                    game_state.particles.append(Particle(hit_heart.x, hit_heart.y, particle_color))
                
                # Create score popup
                game_state.score_popups.append(ScorePopup(hit_heart.x, hit_heart.y, points, combo_multiplier))
                
                # Chance to spawn power-up
                if random.random() < 0.1:  # 10% chance
                    powerup_type = random.choice(['slowmo', 'bomb', 'shield'])
                    game_state.powerups.append(PowerUp(hit_heart.x, hit_heart.y, powerup_type))
                
                hit_heart.reset()
                
                # Level up every 20 hearts
                if game_state.hearts_hit % 20 == 0:
                    game_state.level += 1
                    game_state.spawn_interval = max(15, game_state.spawn_interval - 2)

    if not game_state.game_over and not game_state.paused:
        # Update timers
        if game_state.combo_timer > 0:
            game_state.combo_timer -= 1
        else:
            game_state.combo = 0
        
        if game_state.slowmo_timer > 0:
            game_state.slowmo_timer -= 1
            game_state.game_speed = 0.5
        else:
            game_state.game_speed = 1.0
        
        if game_state.shield_timer > 0:
            game_state.shield_timer -= 1
        
        # Spawn hearts
        game_state.spawn_timer += 2 * game_state.game_speed
        if game_state.spawn_timer >= game_state.spawn_interval:
            game_state.hearts.append(Heart())
            game_state.spawn_timer = 0

        # Update hearts
        landed_hearts = [heart for heart in game_state.hearts if heart.landed]
        for heart in game_state.hearts:
            old_speed = heart.speed
            heart.speed = int(old_speed * game_state.game_speed)
            heart.update(landed_hearts)
            heart.speed = old_speed

        # Check game over condition
        for heart in game_state.hearts:
            danger_line = HEIGHT // 2 + 50
            if heart.landed and heart.y <= danger_line:
                if game_state.shield_timer > 0:
                    # Shield protects - remove some hearts
                    game_state.hearts = [h for h in game_state.hearts if not h.landed or h.y > danger_line]
                    game_state.shield_timer = 0
                else:
                    game_state.lives -= 1
                    if game_state.lives <= 0:
                        game_state.game_over = True
                    else:
                        # Remove some hearts to give player a chance
                        game_state.hearts = [h for h in game_state.hearts if not h.landed or h.y > danger_line]
                    break
        
        # Update power-ups
        for powerup in game_state.powerups[:]:
            powerup.update()
            if powerup.y > HEIGHT or powerup.lifetime <= 0:
                game_state.powerups.remove(powerup)
            elif math.hypot(pygame.mouse.get_pos()[0] - powerup.x, 
                           pygame.mouse.get_pos()[1] - powerup.y) < 30:
                # Collect power-up
                if powerup.type == 'slowmo':
                    game_state.slowmo_timer = 180  # 3 seconds
                elif powerup.type == 'bomb':
                    # Remove all non-landed hearts
                    for heart in game_state.hearts[:]:
                        if not heart.landed:
                            game_state.particles.extend([Particle(heart.x, heart.y, (255, 100, 100)) for _ in range(5)])
                            game_state.hearts.remove(heart)
                elif powerup.type == 'shield':
                    game_state.shield_timer = 300  # 5 seconds
                game_state.powerups.remove(powerup)
    
    # Update particles
    for particle in game_state.particles[:]:
        particle.update()
        if particle.lifetime <= 0:
            game_state.particles.remove(particle)
    
    # Update score popups
    for popup in game_state.score_popups[:]:
        popup.update()
        if popup.lifetime <= 0:
            game_state.score_popups.remove(popup)

    # Drawing
    screen.blit(BG_IMAGE, (0, 0))
    
    # Draw danger line with pulsing effect
    danger_line = HEIGHT // 2 + 50
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 30 + 50
    danger_color = (255, int(pulse), int(pulse))
    pygame.draw.line(screen, danger_color, (0, danger_line), (WIDTH, danger_line), 3)
    
    # Draw hearts
    for heart in game_state.hearts:
        heart.draw(screen)
    
    # Draw particles
    for particle in game_state.particles:
        particle.draw(screen)
    
    # Draw power-ups
    for powerup in game_state.powerups:
        powerup.draw(screen, font)
    
    # Draw score popups
    for popup in game_state.score_popups:
        popup.draw(screen, font)
    
    # Draw UI with better visibility
    # Score
    score_text = f"Score: {game_state.score}"
    score_surface = font.render(score_text, True, (255, 255, 255))
    score_outline = font.render(score_text, True, (0, 0, 0))
    screen.blit(score_outline, (12, 12))
    screen.blit(score_surface, (10, 10))
    
    # High Score
    if game_state.high_score > 0:
        high_score_text = f"Best: {game_state.high_score}"
        high_score_surface = small_font.render(high_score_text, True, (255, 255, 100))
        high_score_outline = small_font.render(high_score_text, True, (0, 0, 0))
        screen.blit(high_score_outline, (12, 42))
        screen.blit(high_score_surface, (10, 40))
    
    # Combo
    if game_state.combo > 1:
        combo_text = f"COMBO x{game_state.combo}!"
        combo_size = 40 + int(abs(math.sin(pygame.time.get_ticks() * 0.01)) * 5)
        combo_font = pygame.font.SysFont(None, combo_size)
        combo_surface = combo_font.render(combo_text, True, (255, 200, 0))
        combo_outline = combo_font.render(combo_text, True, (255, 0, 0))
        x = WIDTH // 2 - combo_surface.get_width() // 2
        screen.blit(combo_outline, (x + 2, 52))
        screen.blit(combo_surface, (x, 50))
    
    # Level
    level_text = f"Level {game_state.level}"
    level_surface = font.render(level_text, True, (255, 255, 255))
    level_outline = font.render(level_text, True, (0, 0, 0))
    screen.blit(level_outline, (WIDTH - level_surface.get_width() - 8, 12))
    screen.blit(level_surface, (WIDTH - level_surface.get_width() - 10, 10))
    
    # Lives
    lives_text = f"Lives: "
    lives_surface = font.render(lives_text, True, (255, 255, 255))
    lives_outline = font.render(lives_text, True, (0, 0, 0))
    screen.blit(lives_outline, (WIDTH - 122, 42))
    screen.blit(lives_surface, (WIDTH - 124, 40))
    
    # Draw heart icons for lives
    for i in range(game_state.lives):
        heart_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(heart_icon, (255, 0, 100), (7, 9), 5)
        pygame.draw.circle(heart_icon, (255, 0, 100), (13, 9), 5)
        pygame.draw.polygon(heart_icon, (255, 0, 100), [(3, 9), (17, 9), (10, 18)])
        screen.blit(heart_icon, (WIDTH - 60 + i * 22, 44))
    
    # Active power-ups indicator
    y_offset = 70
    if game_state.slowmo_timer > 0:
        slowmo_text = f"SLOW-MO: {game_state.slowmo_timer // 60 + 1}s"
        slowmo_surface = small_font.render(slowmo_text, True, (100, 200, 255))
        screen.blit(slowmo_surface, (WIDTH - 150, y_offset))
        y_offset += 25
    
    if game_state.shield_timer > 0:
        shield_text = f"SHIELD: {game_state.shield_timer // 60 + 1}s"
        shield_surface = small_font.render(shield_text, True, (100, 255, 100))
        screen.blit(shield_surface, (WIDTH - 150, y_offset))
    
    # Pause screen
    if game_state.paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        pause_surface = title_font.render("PAUSED", True, (255, 255, 255))
        continue_surface = font.render("Press SPACE to Continue", True, (200, 200, 200))
        
        screen.blit(pause_surface, (WIDTH // 2 - pause_surface.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(continue_surface, (WIDTH // 2 - continue_surface.get_width() // 2, HEIGHT // 2 + 20))
    
    # Game over screen
    if game_state.game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_surface = title_font.render("GAME OVER", True, (255, 50, 50))
        final_score_surface = font.render(f"Final Score: {game_state.score}", True, (255, 255, 255))
        level_reached_surface = font.render(f"Level Reached: {game_state.level}", True, (200, 200, 200))
        restart_surface = font.render("Press R to Restart", True, (100, 255, 100))
        
        if game_state.score > game_state.high_score:
            new_high_surface = font.render("NEW HIGH SCORE!", True, (255, 215, 0))
            screen.blit(new_high_surface, (WIDTH // 2 - new_high_surface.get_width() // 2, HEIGHT // 2 - 100))
        
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(final_score_surface, (WIDTH // 2 - final_score_surface.get_width() // 2, HEIGHT // 2))
        screen.blit(level_reached_surface, (WIDTH // 2 - level_reached_surface.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()

pygame.quit()
sys.exit()
