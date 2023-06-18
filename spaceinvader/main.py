import pygame
import random

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

white = (255, 255, 255)
black = (0, 0, 0)

#----Player----
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect)

#----Bullet----
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect)

#----Enemy----
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-500, -50)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-500, -50)
        self.speed_y = random.randint(1, 3)

    def draw(self, screen):
        pygame.draw.rect(screen, self.image.fill, self.rect)

player = Player()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for _ in range(10):
    enemy = Enemy()
    enemies.add(enemy)

#----Game loop----
clock = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

    player.update()
    bullets.update()
    enemies.update()

    #----collision between bullets and enemies----
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet, enemies, True):
            bullet.kill()

    #----collision between player and enemies----
    if pygame.sprite.spritecollide(player, enemies, True):
        running = False

    #----Respawn enemies----
    if len(enemies) == 0:
        for _ in range(10):
            enemy = Enemy()
            enemies.add(enemy)

    screen.fill(black)
    player.draw(screen)
    bullets.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()