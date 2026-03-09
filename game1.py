# shadow_runner.py
# Side-scrolling runner "Shadow Runner"
# Requirements: python3, pygame
# Run: python3 shadow_runner.py

import pygame, random, sys, math, os

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 900, 500
FPS = 60
GROUND_Y = HEIGHT - 80

# Player physics
PLAYER_X = 140
PLAYER_W, PLAYER_H = 44, 56
JUMP_VELOCITY = -12
GRAVITY = 0.6

# World
INITIAL_SCROLL = 5.0
SCROLL_ACCEL = 0.002  # increases scroll speed over time
OBSTACLE_FREQ = 1200  # ms (initial)
COIN_FREQ = 900       # ms

# Colors
WHITE = (255,255,255)
BLACK = (12,12,12)
SKY = (90,155,255)
GROUND = (40,30,30)
PLAYER_COL = (50,200,80)
SHADOW_COL = (200,40,40)
OB_COL = (80,80,80)
COIN_COL = (255,205,0)
TEXT_COL = (230,230,230)

# Files
HIGHSCORE_FILE = "shadow_highscore.txt"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Runner")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 28)
BIG = pygame.font.SysFont(None, 64)

# ---------------- Helpers ----------------
def draw_text(surf, txt, pos, size=None, center=False, color=TEXT_COL):
    f = BIG if size == "big" else FONT
    img = f.render(txt, True, color)
    if center:
        rect = img.get_rect(center=pos)
        surf.blit(img, rect)
    else:
        surf.blit(img, pos)

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(score):
    try:
        cur = load_highscore()
        if score > cur:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(score))
    except:
        pass

# ---------------- Entities ----------------
class Player:
    def __init__(self):
        self.x = PLAYER_X
        self.y = GROUND_Y - PLAYER_H
        self.w = PLAYER_W
        self.h = PLAYER_H
        self.vy = 0
        self.on_ground = True
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False
    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True
        self.rect.topleft = (int(self.x), int(self.y))
    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COL, self.rect, border_radius=6)
        # eye
        pygame.draw.circle(surf, BLACK, (self.rect.centerx+6, self.rect.centery-6), 3)

class ShadowChaser:
    def __init__(self):
        # initially behind player
        self.x = PLAYER_X - 140
        self.y = GROUND_Y - 56
        self.size = 52
        self.speed = 3.0
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
    def update(self, player_x, player_y, scroll):
        # chase logic: move right if too far behind, but world scroll pulls everything left
        # we adapt speed slightly based on scroll to remain a threat
        target_x = player_x - 100
        dx = target_x - self.x
        # move horizontally towards target_x
        if abs(dx) > 1:
            self.x += math.copysign(min(abs(dx)*0.02 + 0.6, 4.0), dx) + (scroll - INITIAL_SCROLL)*0.1
        # vertical follow: stand on ground
        self.y = GROUND_Y - self.size
    def draw(self, surf):
        r = self.rect()
        pygame.draw.ellipse(surf, SHADOW_COL, r)
        # eyes
        pygame.draw.circle(surf, (10,10,10), (r.centerx+6, r.centery-8), 4)

class Obstacle:
    def __init__(self, x, w, h):
        self.x = x
        self.w = w
        self.h = h
        self.y = GROUND_Y - h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def update(self, scroll):
        self.x -= scroll
        self.rect.topleft = (int(self.x), int(self.y))
    def draw(self, surf):
        pygame.draw.rect(surf, OB_COL, self.rect, border_radius=6)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 9
        self.rect = pygame.Rect(x - self.r, y - self.r, 2*self.r, 2*self.r)
    def update(self, scroll):
        self.x -= scroll
        self.rect.topleft = (int(self.x - self.r), int(self.y - self.r))
    def draw(self, surf):
        pygame.draw.circle(surf, COIN_COL, (int(self.x), int(self.y)), self.r)

# ---------------- Screens ----------------
def start_screen():
    while True:
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        draw_text(screen, "Shadow Runner", (WIDTH//2, 80), size="big", center=True)
        draw_text(screen, "Jump over obstacles. Collect coins. Don't let the shadow catch you.", (WIDTH//2 - 220, 160))
        draw_text(screen, "Controls: Space / Up to jump. P to pause. Enter to start.", (WIDTH//2 - 220, 200))
        draw_text(screen, "Choose difficulty: 1-Easy  2-Normal  3-Hard", (WIDTH//2 - 220, 240))
        cur = load_highscore()
        draw_text(screen, f"High Score: {cur}", (WIDTH - 180, 20))
        draw_text(screen, "Press Enter to start (Default: Normal).", (WIDTH//2 - 220, 300))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return 2  # default normal
                if e.key == pygame.K_1:
                    return 1
                if e.key == pygame.K_2:
                    return 2
                if e.key == pygame.K_3:
                    return 3
                if e.key == pygame.K_h:
                    help_screen()

def help_screen():
    while True:
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        draw_text(screen, "HELP", (WIDTH//2, 80), size="big", center=True)
        draw_text(screen, "- The player runs automatically. You can jump to avoid obstacles.", (120, 160))
        draw_text(screen, "- Collect coins for points. The shadow chases from behind.", (120, 190))
        draw_text(screen, "- The world speeds up over time.", (120, 220))
        draw_text(screen, "Press B to go back.", (WIDTH//2 - 80, 300))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_b:
                return

def game_over_screen(score):
    save_highscore(score)
    hs = load_highscore()
    while True:
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", (WIDTH//2, 120), size="big", center=True)
        draw_text(screen, f"Score: {score}", (WIDTH//2 - 40, 200), center=True)
        draw_text(screen, f"High Score: {hs}", (WIDTH//2 - 60, 240), center=True)
        draw_text(screen, "Enter to play again. Q to quit.", (WIDTH//2 - 130, 320), center=True)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return True
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# ---------------- Main Game Loop ----------------
def run_game(difficulty):
    # difficulty tweaks
    scroll = INITIAL_SCROLL * (1 + (difficulty - 2)*0.18)  # easy <-> hard scale
    shadow = ShadowChaser()
    player = Player()
    obstacles = []
    coins = []
    score = 0
    dist = 0.0
    last_ob = pygame.time.get_ticks()
    last_coin = pygame.time.get_ticks()
    running = True
    paused = False

    while running:
        dt = clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_UP):
                    player.jump()
                if e.key == pygame.K_p:
                    paused = not paused

        if paused:
            draw_text(screen, "PAUSED - Press P to resume", (WIDTH//2 - 120, HEIGHT//2), center=False)
            pygame.display.flip()
            continue

        # update scroll speed gradually
        scroll += SCROLL_ACCEL * dt
        dist += scroll * dt * 0.01  # distance metric used as part of score

        # spawn obstacles
        now = pygame.time.get_ticks()
        ob_interval = OBSTACLE_FREQ - int((scroll - INITIAL_SCROLL)*40)  # faster scroll => more frequent
        ob_interval = max(550, ob_interval)
        if now - last_ob > ob_interval:
            # create obstacle offscreen to right
            w = random.randint(30, 70)
            h = random.randint(30, 90)
            x = WIDTH + random.randint(20, 160)
            obstacles.append(Obstacle(x, w, h))
            last_ob = now

        # spawn coins
        coin_interval = COIN_FREQ - int((scroll - INITIAL_SCROLL)*30)
        coin_interval = max(350, coin_interval)
        if now - last_coin > coin_interval:
            x = WIDTH + random.randint(30, 200)
            y = random.randint(GROUND_Y - 180, GROUND_Y - 80)
            coins.append(Coin(x, y))
            last_coin = now

        # updates
        player.update()
        shadow.update(player.x, player.y, scroll)

        for ob in obstacles[:]:
            ob.update(scroll)
            if ob.rect.right < -50:
                obstacles.remove(ob)
        for c in coins[:]:
            c.update(scroll)
            if c.rect.right < -30:
                coins.remove(c)

        # collisions: player with obstacles
        for ob in obstacles:
            if player.rect.colliderect(ob.rect):
                # collision → game over
                return False, int(score + dist)

        # collisions: player with coins
        for c in coins[:]:
            if player.rect.colliderect(c.rect):
                coins.remove(c)
                score += 10

        # shadow touches player?
        if player.rect.colliderect(shadow.rect()):
            return False, int(score + dist)

        # draw world
        screen.fill(SKY)
        pygame.draw.rect(screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

        # draw coins & obstacles
        for c in coins:
            c.draw(screen)
        for ob in obstacles:
            ob.draw(screen)

        # draw player and shadow
        shadow.draw(screen)
        player.draw(screen)

        # HUD
        total = int(score + dist)
        draw_text(screen, f"Score: {total}", (12, 12))
        draw_text(screen, f"Distance: {int(dist)}", (12, 36))
        draw_text(screen, f"Speed: {scroll:.1f}", (12, 60))
        draw_text(screen, "P: Pause  Space/Up: Jump", (WIDTH - 320, 12))
        pygame.display.flip()

    return False, int(score + dist)

# ---------------- Entry ----------------
def main():
    while True:
        difficulty = start_screen()
        win, score = run_game(difficulty)
        # run_game returns (False, score) on game-over
        game_over_screen(score)

if __name__ == "__main__":
    main()
