import pygame
from pygame.locals import *
import random

# start pygame
pygame.init()
pygame.font.init()
title_font = pygame.font.Font(size = 50)
game_font = pygame.font.Font(size=30)

# get screen with width and height
W, H = 1200, 800
screen = pygame.display.set_mode((W, H))

# get clock for frame setting
clock = pygame.time.Clock()

# write title
title = title_font.render('Fruit Collector Game', True, 'black', 'white')

# write instructions
instructions = game_font.render('Move with WASD. Collect fruit.', True, 'blue', 'white')

# write fruit counter
fruit_count = 0
fruit_counter = game_font.render(f'Fruits Caught: {fruit_count}', True, 'blue', 'white')

# collect all text in a list
texts = [title, instructions, fruit_counter]

# set movable area with enclosure
thic = 10
offset = max(texts, key = lambda a: a.get_height()).get_height() + 30
movable_area = pygame.Surface((W, H - offset))
pygame.draw.rect(movable_area, 'white', movable_area.get_rect(), width = thic)

# make a cirlce
rad = 50
player_pos = [W//2, H//2]
player = pygame.draw.circle(screen, color = 'red', center = player_pos, radius = rad)
movement_speed = [10,10]

# make a fruit
fruit_w, fruit_h = 20, 20
fruit_exists = True
fruit = pygame.Rect(random.randint(thic, W - thic - fruit_w), random.randint(thic, H - thic - fruit_h - offset), fruit_w, fruit_h)
pygame.draw.rect(movable_area, 'yellow', fruit)

# count number of frames from last collection
frames_passed = 0

# main game loop
running = True
while running:
    # if player clicks X then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ###############################
    # Game logic updates
    ###############################
    # move circle position based on WASD keystrokes
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= movement_speed[1]
    if keys[pygame.K_a]:
        player_pos[0] -= movement_speed[0]
    if keys[pygame.K_s]:
        player_pos[1] += movement_speed[1]
    if keys[pygame.K_d]:
        player_pos[0] += movement_speed[1]
    
    # make sure player cannot move off screen
    enclosure = rad+thic
    if player_pos[0] + enclosure > W:
        player_pos[0] = W - enclosure
    if player_pos[0] < enclosure:
        player_pos[0] = enclosure
    if player_pos[1] + enclosure + offset > H:
        player_pos[1] = H - enclosure - offset
    if player_pos[1] < enclosure:
        player_pos[1] = enclosure

    # if the circle collected fruit, then increment fruit counter by 1 and fruit no longer exists
    if player.colliderect(fruit):
        fruit_exists = False
        fruit_count += 1
        fruit_counter = game_font.render(f'     Fruits Caught: {fruit_count}      ', True, 'blue', 'white')

        # move fruit off screen while waiting
        fruit = pygame.Rect(-1000, -1000, fruit_w, fruit_h)

    # if the fruit was caught and enough time passed, generate another fruit
    if not fruit_exists and frames_passed >= 100:
        fruit_exists = True
        fruit = pygame.Rect(random.randint(thic, W - thic - fruit_w), random.randint(thic, H - thic - fruit_h - offset), fruit_w, fruit_h)
        frames_passed = 0
    else:
        frames_passed += 1

    ###############################
    # Screen updates
    ###############################
    # clear screen
    screen.fill('white')
    movable_area.fill('black')

    # graphics changes
    # write the title
    screen.blit(title, (W//2 - title.get_width()//2, title.get_height()//2))
    # write the instructions
    screen.blit(instructions, (20, title.get_height()//2))
    # write the fruit counter
    screen.blit(fruit_counter, (W-fruit_counter.get_width()-20, title.get_height()//2))

    # draw encloure for the circle
    pygame.draw.rect(movable_area, 'white', movable_area.get_rect(), width = 10)

    # draw the fruit
    if fruit_exists:
        pygame.draw.rect(movable_area, 'yellow', fruit)

    # draw the circle at the new position
    player = pygame.draw.circle(movable_area, color = 'red', center = player_pos, radius = rad)
    screen.blit(movable_area, (0, offset))

    # show renderd graphics
    pygame.display.flip()

    # limit fps to 60
    clock.tick(60)

pygame.quit()