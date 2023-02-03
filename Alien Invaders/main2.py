import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # 800px width 600px height

# background
background = pygame.image.load('space.jpg') # background image
mixer.music.load('background.wav') # background music
mixer.music.play(-1) # loops the music

# title and icon
pygame.display.set_caption('Space Invaders') # title
icon = pygame.image.load('ufo.png') # icon
pygame.display.set_icon(icon)

# level
level_value = 1
level = pygame.font.Font("freesansbold.ttf", 32)
level_textX = 650
level_textY = 10

def show_level(x, y):
    level_text = level.render("Level " + str(level_value), True, (255, 255, 255))
    screen.blit(level_text, (x, y))

    
# player
playerImg = pygame.image.load('ship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5 # number of enemies

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5) # enemy X axis speed
    enemyY_change.append(50) # enemy Y axis speed

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2 # bullet speed
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
# game loop
running = True
while running:

    # RGB - Red Green Blue
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (-550, -100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -1 # player moving speed
        if event.key == pygame.K_RIGHT:
            playerX_change = 1 # player moving speed
        if event.key == pygame.K_UP:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(playerX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
        
        enemy(enemyX[i], enemyY[i], i)
    
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    show_level(level_textX, level_textY)
    pygame.display.update()