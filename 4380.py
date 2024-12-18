import pygame
import sys
import random
import json

# Dosya yolları
selim_image_path = "43man.png"
food_image_path = "tckimlik.png"
sound_path = "tckimlik.mp3"
game_over_sound_path = "4380.mp3"
powerup_image_path = "powerup.gif"
background_image_path = "background.jpg"

pygame.init()
pygame.mixer.init()

# Ekran ayarları
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("4380man")

# Renkler
screenColor = (0, 0, 0)
textColor = (255, 255, 255)
buttonColor = (50, 50, 200)
buttonHoverColor = (100, 100, 250)

# Görseller
selim_img = pygame.image.load(selim_image_path)
selim_img = pygame.transform.scale(selim_img, (50, 50))
food_img = pygame.image.load(food_image_path)
food_img = pygame.transform.scale(food_img, (50, 50))
powerup_img = pygame.image.load(powerup_image_path)
powerup_img = pygame.transform.scale(powerup_img, (30, 30))
background_img = pygame.image.load(background_image_path)
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Sesler
eat_sound = pygame.mixer.Sound(sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# Oyuncu ve oyun ayarları
selim_x, selim_y = 375, 275
selim_speed = 5
selim_size = 50
food_speed = 2
time_limit = 20
food_positions = [(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)) for _ in range(10)]
food_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(len(food_positions))]

# Engeller
obstacle_positions = [(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)) for _ in range(5)]

# Güçlendirici ayarları
powerup_position = (random.randint(0, screen_width - 30), random.randint(0, screen_height - 30))
powerup_active = False
powerup_duration = 5000  # 5 saniye
time_powerup_activated = 0

# Skor
score = 0
level = 1

# Yüksek Skorlar
score_file = "highscores.json"
try:
    with open(score_file, "r") as f:
        highscores = json.load(f)
except FileNotFoundError:
    highscores = []

# Font
font = pygame.font.Font(None, 36)

# Saat
clock = pygame.time.Clock()

# Oyun durumları
running = True
game_over = False
game_started = False
difficulty_selected = True  # Zorluk otomatik "Kolay" olarak ayarlı

# Buton fonksiyonu
def draw_button(screen, text, x, y, width, height, font, base_color, hover_color, mouse_pos):
    rect = pygame.Rect(x, y, width, height)
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect)
    button_text = font.render(text, True, textColor)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))
    return rect

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_started:
            game_started = True
            start_time = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Oyunu yeniden başlat
                game_over = False
                score = 0
                level = 1
                selim_x, selim_y = 375, 275
                selim_size = 50
                selim_speed = 5
                food_positions = [(random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)) for _ in range(10)]
                food_directions = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(len(food_positions))]
                obstacle_positions = [(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)) for _ in range(5)]
                powerup_position = (random.randint(0, screen_width - 30), random.randint(0, screen_height - 30))
                start_time = pygame.time.get_ticks()

    # Arka plan
    screen.blit(background_img, (0, 0))

    if game_started and not game_over:
        # Zaman kontrolü
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time >= time_limit:
            game_over = True
            game_over_sound.play()

        # Oyuncu hareketi
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: selim_y -= selim_speed
        if keys[pygame.K_DOWN]: selim_y += selim_speed
        if keys[pygame.K_LEFT]: selim_x -= selim_speed
        if keys[pygame.K_RIGHT]: selim_x += selim_speed

        selim_x = max(0, min(screen_width - selim_size, selim_x))
        selim_y = max(0, min(screen_height - selim_size, selim_y))

        # Yemek hareketi ve kontrol
        new_food_positions = []
        for idx, (fx, fy) in enumerate(food_positions):
            dx, dy = food_directions[idx]
            fx += food_speed * dx
            fy += food_speed * dy

            if fx <= 0 or fx >= screen_width - 30:
                food_directions[idx] = (-dx, dy)
            if fy <= 0 or fy >= screen_height - 30:
                food_directions[idx] = (dx, -dy)

            # Yemek yendi mi kontrol et
            if selim_x < fx + 30 and selim_x + selim_size > fx and selim_y < fy + 30 and selim_y + selim_size > fy:
                eat_sound.play()
                score += 1
                selim_size += 2
                selim_speed = max(1, selim_speed - 0.1)
                food_speed += 0.05

                # Yeni yemek oluştur
                new_food_positions.append((random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)))
            else:
                new_food_positions.append((fx, fy))
        food_positions = new_food_positions

        # Engelleri kontrol et ve çiz
        for ox, oy in obstacle_positions:
            pygame.draw.rect(screen, (255, 0, 0), (ox, oy, 50, 50))
            if selim_x < ox + 50 and selim_x + selim_size > ox and selim_y < oy + 50 and selim_y + selim_size > oy:
                game_over = True
                game_over_sound.play()

        # Skor ve seviyeyi kontrol et
        if score > level * 9:
            level += 1
            food_speed += 0.1
            obstacle_positions.append((random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)))

        # Oyuncuyu ve yemleri çiz
        scaled_selim_img = pygame.transform.scale(selim_img, (selim_size, selim_size))
        screen.blit(scaled_selim_img, (selim_x, selim_y))
        for fx, fy in food_positions:
            screen.blit(food_img, (fx, fy))

        # Güçlendirici kontrolü ve çizimi
        if powerup_active and pygame.time.get_ticks() - time_powerup_activated > powerup_duration:
            selim_speed = 5
            powerup_active = False
            powerup_position = (random.randint(0, screen_width - 30), random.randint(0, screen_height - 30))

        if not powerup_active:
            px, py = powerup_position
            screen.blit(powerup_img, powerup_position)
            if selim_x < px + 30 and selim_x + selim_size > px and selim_y < py + 30 and selim_y + selim_size > py:
                powerup_active = True
                selim_speed = 8
                time_powerup_activated = pygame.time.get_ticks()

        # Skor, seviye ve zaman bilgisi
        score_text = font.render(f"TC KİMLİK SAYACI: {score}", True, textColor)
        level_text = font.render(f"Seviye: {level}", True, textColor)
        remaining_time = max(0, time_limit - int(elapsed_time))
        time_text = font.render(f"Kalan Süre: {remaining_time}sn", True, textColor)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(time_text, (10, 70))

    elif game_over:
        # Oyun bitti ekranı
        game_over_text = font.render("TC KİMLİK AVI BİTTİ!", True, textColor)
        restart_text = font.render("Tekrar Oynamak için 'R'ye bas", True, textColor)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
