import pygame
import sys
import random

pacman_image_path = "43man.png"
food_image_path = "tckimlik.png"
sound_path = "tckimlik.mp3" 
game_over_sound_path = "4380.mp3"

pygame.init()
pygame.mixer.init()  

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("4380man")

screenColor = (0, 0, 0)

selim_img = pygame.image.load(pacman_image_path)
selim_img = pygame.transform.scale(selim_img, (50, 50))
food_img = pygame.image.load(food_image_path)
food_img = pygame.transform.scale(food_img, (30, 30))

eat_sound = pygame.mixer.Sound(sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

selim_x, selim_y = 375, 275
selim_speed = 5

food_positions = [(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)) for _ in range(10)]

score = 0

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            selim_y -= selim_speed
        if keys[pygame.K_DOWN]:
            selim_y += selim_speed
        if keys[pygame.K_LEFT]:
            selim_x -= selim_speed
        if keys[pygame.K_RIGHT]:
            selim_x += selim_speed

        # sınırları kontrol ediyo
        selim_x = max(0, min(screen_width - 50, selim_x))
        selim_y = max(0, min(screen_height - 50, selim_y))

        # Yemleri yeme kontrolü
        new_food_positions = []
        for fx, fy in food_positions:
            if not (selim_x < fx + 30 and selim_x + 50 > fx and selim_y < fy + 30 and selim_y + 50 > fy):
                new_food_positions.append((fx, fy))
            else:
                eat_sound.play()
                score += 1
                new_food = (random.randint(0, screen_width - 30), random.randint(0, screen_height - 30))
                new_food_positions.append(new_food)

        food_positions = new_food_positions

        if score >= 10:
            game_over = True
            game_over_sound.play()  

    # Ekranı çiz
    screen.fill(screenColor)
    if not game_over:
        screen.blit(selim_img, (selim_x, selim_y))
        for fx, fy in food_positions:
            screen.blit(food_img, (fx, fy))
        score_text = font.render(f"TC KİMLİK SAYAC: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    else:
        game_over_text = font.render("TC KİMLİK SON 2 RAKAM 4380", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
