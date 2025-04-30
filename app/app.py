import pygame
import time
import random
import sys
import os
from datetime import datetime

pygame.init()

# Définir les dimensions de la fenêtre
window_x = 720
window_y = 480

# Créer la fenêtre du jeu
pygame.display.set_caption('Snakes')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Chemin vers le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chargement d’images
def load_image(name, size=(10, 10)):
    return pygame.transform.scale(pygame.image.load(os.path.join(script_dir, name)), size)

def load_background(name):
    return pygame.transform.scale(pygame.image.load(os.path.join(script_dir, name)), (window_x, window_y))

# Sprites
apple_image = load_image('apple.png')
herbe = load_background('grace.png')

# Corps
body_horizontal = load_image('body_horizontal.png')
body_vertical = load_image('body_vertical.png')
body_topleft = load_image('body_topleft.png')
body_topright = load_image('body_topright.png')
body_bottomleft = load_image('body_bottomleft.png')
body_bottomright = load_image('body_bottomright.png')

# Tête
head_up = load_image('head_up.png')
head_down = load_image('head_down.png')
head_left = load_image('head_left.png')
head_right = load_image('head_right.png')

# Queue
tail_up = load_image('tail_up.png')
tail_down = load_image('tail_down.png')
tail_left = load_image('tail_left.png')
tail_right = load_image('tail_right.png')

# Couleurs
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Variables globales
paused = False
gameover = False
pseudo = ""
score = 0

# Affichage du score
def show_score(choice, color, font, size):
    global score
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Enregistrement du score
def save_score(score, pseudo):
    try:
        with open(os.path.join(script_dir, "scores.txt"), "a") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{pseudo} - {score} - {current_time}\n")
    except:
        pass

# Récupérer derniers scores
def get_last_scores():
    try:
        with open(os.path.join(script_dir, "scores.txt"), "r") as f:
            lines = f.readlines()
        return lines[-3:][::-1]
    except:
        return []

# Récupérer top scores
def get_top_scores():
    try:
        with open(os.path.join(script_dir, "scores.txt"), "r") as f:
            lines = f.readlines()
        scores = []
        for line in lines:
            parts = line.strip().split(" - ")
            if len(parts) == 3:
                pseudo, score, _ = parts
                try:
                    scores.append((pseudo, int(score)))
                except ValueError:
                    continue
        return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
    except:
        return []

# Écran d'introduction
def display_intro():
    global pseudo
    font = pygame.font.SysFont('times new roman', 50)
    small_font = pygame.font.SysFont('times new roman', 30)
    tiny_font = pygame.font.SysFont('times new roman', 24)

    intro_text = font.render("Entrez votre pseudo", True, white)
    intro_rect = intro_text.get_rect(center=(window_x / 2, window_y / 3))
    recent_scores = get_last_scores()
    top_scores = get_top_scores()
    recent_title = tiny_font.render("Scores récents", True, white)
    top_title = tiny_font.render("Meilleurs scores", True, white)

    recent_title_rect = recent_title.get_rect(midright=(window_x / 3.2, window_y / 3 - 150))
    top_title_rect = top_title.get_rect(midleft=(3 * window_x / 4, window_y / 3 - 150))

    pseudo = ""

    while len(pseudo) < 3:
        game_window.fill(black)
        game_window.blit(intro_text, intro_rect)
        game_window.blit(recent_title, recent_title_rect)
        game_window.blit(top_title, top_title_rect)

        for i, line in enumerate([pygame.font.SysFont('times new roman', 24).render(score.strip(), True, white) for score in recent_scores]):
            rect = line.get_rect(midright=(window_x / 2.2, window_y / 3 - 120 + i * 25))
            game_window.blit(line, rect)

        for i, line in enumerate([pygame.font.SysFont('times new roman', 24).render(f"{p} - {s}", True, white) for p, s in top_scores]):
            rect = line.get_rect(midleft=(3 * window_x / 4, window_y / 3 - 120 + i * 25))
            game_window.blit(line, rect)

        display_text = " ".join(pseudo.ljust(3, "_"))
        text = small_font.render(display_text, True, white)
        rect = text.get_rect(center=(window_x / 2, window_y / 2))
        game_window.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                elif len(pseudo) < 3 and event.unicode.isalpha():
                    pseudo += event.unicode.upper()

    while True:
        game_window.fill(black)
        confirm_text = small_font.render(f"Pseudo : {pseudo}", True, white)
        modif_text = small_font.render("Appuyez sur M pour modifier", True, white)
        start_text = small_font.render("Appuyez sur Entrée pour jouer", True, white)
        game_window.blit(confirm_text, confirm_text.get_rect(center=(window_x / 2, window_y / 3)))
        game_window.blit(modif_text, modif_text.get_rect(center=(window_x / 2, window_y / 2)))
        game_window.blit(start_text, start_text.get_rect(center=(window_x / 2, window_y / 2 + 40)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pseudo = ""
                    return display_intro()
                if event.key == pygame.K_RETURN:
                    game_loop()
                    return

# Menu pause ou game over
def menu():
    global paused, gameover, score
    font = pygame.font.SysFont('times new roman', 50)
    small_font = pygame.font.SysFont('times new roman', 30)

    if not gameover:
        menu_surface = font.render('Paused', True, red)
        resume_surface = small_font.render('Press ESC to resume', True, white)
        resume_rect = resume_surface.get_rect(center=(window_x / 2, window_y / 3 + 25))
    else:
        menu_surface = font.render('GAME OVER', True, red)
        save_score(score, pseudo)

    menu_rect = menu_surface.get_rect(center=(window_x / 2, window_y / 8))
    score_surface = small_font.render('Score : ' + str(score), True, green)
    score_rect = score_surface.get_rect(center=(window_x / 2, window_y / 4))
    restart_surface = small_font.render('Press R to Restart', True, white)
    restart_rect = restart_surface.get_rect(center=(window_x / 2, window_y / 3 + 75))
    quit_surface = small_font.render('Press Q to Quit', True, white)
    quit_rect = quit_surface.get_rect(center=(window_x / 2, window_y / 3 + 125))

    while True:
        game_window.fill(black)
        if not gameover:
            game_window.blit(resume_surface, resume_rect)
        game_window.blit(menu_surface, menu_rect)
        game_window.blit(score_surface, score_rect)
        game_window.blit(restart_surface, restart_rect)
        game_window.blit(quit_surface, quit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                elif event.key == pygame.K_r: game_loop()
                elif event.key == pygame.K_q: pygame.quit(); sys.exit()
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

# Boucle principale du jeu
def game_loop():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score, snake_speed, gameover, pseudo

    gameover = False
    score = 0
    snake_speed = 7

    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: change_to = 'UP'
                if event.key == pygame.K_DOWN: change_to = 'DOWN'
                if event.key == pygame.K_LEFT: change_to = 'LEFT'
                if event.key == pygame.K_RIGHT: change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE: menu()
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

        if direction == 'UP': snake_position[1] -= 10
        if direction == 'DOWN': snake_position[1] += 10
        if direction == 'LEFT': snake_position[0] -= 10
        if direction == 'RIGHT': snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            snake_speed += 2
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        game_window.blit(herbe, (0, 0))  # Fond

        for i, pos in enumerate(snake_body):
            if i == 0:
                game_window.blit({'UP': head_up, 'DOWN': head_down, 'LEFT': head_left, 'RIGHT': head_right}[direction], pos)
            elif i == len(snake_body) - 1:
                prev = snake_body[i - 1]
                if prev[1] > pos[1]: game_window.blit(tail_up, pos)
                elif prev[1] < pos[1]: game_window.blit(tail_down, pos)
                elif prev[0] > pos[0]: game_window.blit(tail_left, pos)
                elif prev[0] < pos[0]: game_window.blit(tail_right, pos)
            else:
                prev = snake_body[i - 1]
                nxt = snake_body[i + 1] if i + 1 < len(snake_body) else prev
                if prev[0] == nxt[0]: game_window.blit(body_vertical, pos)
                elif prev[1] == nxt[1]: game_window.blit(body_horizontal, pos)
                else:
                    if (prev[0] < pos[0] and nxt[1] < pos[1]) or (nxt[0] < pos[0] and prev[1] < pos[1]):
                        game_window.blit(body_topleft, pos)
                    elif (prev[0] > pos[0] and nxt[1] < pos[1]) or (nxt[0] > pos[0] and prev[1] < pos[1]):
                        game_window.blit(body_topright, pos)
                    elif (prev[0] < pos[0] and nxt[1] > pos[1]) or (nxt[0] < pos[0] and prev[1] > pos[1]):
                        game_window.blit(body_bottomleft, pos)
                    elif (prev[0] > pos[0] and nxt[1] > pos[1]) or (nxt[0] > pos[0] and prev[1] > pos[1]):
                        game_window.blit(body_bottomright, pos)

        game_window.blit(apple_image, fruit_position)

        if snake_position[0] < 0 or snake_position[0] > window_x - 10 or snake_position[1] < 0 or snake_position[1] > window_y - 10:
            gameover = True
            menu()

        for block in snake_body[1:]:
            if snake_position == block:
                gameover = True
                menu()

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

# Lancer le jeu
display_intro()
