import pygame
import time
import random
import sys
import os
from datetime import datetime

paused = False
gameover = False

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

pseudo = ""
score = 0  # Ajouté pour éviter un crash si score n'est pas défini ailleurs.

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def save_score(score, pseudo):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "scores.txt")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, "a") as f:
            f.write(f"{pseudo} - {score} - {current_time}\n")
    except:
        pass

def get_last_scores():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "scores.txt")
        with open(file_path, "r") as f:
            lines = f.readlines()
        return [line.split(" - ")[0] + " - " + line.split(" - ")[1] for line in lines[-3:]][::-1]
    except:
        return []

def get_top_scores():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "scores.txt")
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        scores = []
        for line in lines:
            parts = line.strip().split(" - ")
            if len(parts) == 3:
                pseudo, score, _ = parts
                try:
                    score = int(score)
                    scores.append((pseudo, score))
                except ValueError:
                    continue

        top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:3]
        return top_scores
    except:
        return []

def display_intro():
    global pseudo
    my_font = pygame.font.SysFont('times new roman', 50)
    small_font = pygame.font.SysFont('times new roman', 30)
    tiny_font = pygame.font.SysFont('times new roman', 24)

    intro_text = my_font.render("Entrez votre pseudo", True, white)
    intro_rect = intro_text.get_rect(center=(window_x / 2, window_y / 3))

    recent_scores = get_last_scores()
    top_scores = get_top_scores()

    recent_title = tiny_font.render("Scores les plus récents", True, white)
    top_title = tiny_font.render("Meilleurs scores", True, white)

    recent_title_rect = recent_title.get_rect(topleft=(5, window_y / 3 - 150))
    top_title_rect = top_title.get_rect(topright=(window_x - 5, window_y / 3 - 150))

    recent_lines = [tiny_font.render(score.strip(), True, white) for score in recent_scores]
    top_lines = [tiny_font.render(f"{p} - {s}", True, white) for p, s in top_scores]

    pseudo = ""

    while True:
        game_window.fill(black)
        game_window.blit(intro_text, intro_rect)
        game_window.blit(recent_title, recent_title_rect)
        game_window.blit(top_title, top_title_rect)

        for i, line in enumerate(recent_lines):
            rect = line.get_rect(topleft=(5, window_y / 3 - 120 + i * 25))
            game_window.blit(line, rect)
        for i, line in enumerate(top_lines):
            rect = line.get_rect(topright=(window_x - 5, window_y / 3 - 120 + i * 25))
            game_window.blit(line, rect)

        display = " ".join(pseudo.ljust(8, "_"))
        pseudo_text = small_font.render(display, True, white)
        pseudo_rect = pseudo_text.get_rect(center=(window_x / 2, window_y / 2))
        game_window.blit(pseudo_text, pseudo_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                elif event.key == pygame.K_RETURN and len(pseudo) > 0:
                    break  # on sort de la saisie
                elif len(pseudo) < 8 and event.unicode.isalpha():
                    pseudo += event.unicode.upper()

                    # Écran de confirmation
                    while True:
                        game_window.fill(black)

                        confirm_text = small_font.render(f"Pseudo : {pseudo}", True, white)
                        confirm_rect = confirm_text.get_rect(center=(window_x / 2, window_y / 3))
                        modif_text = small_font.render("Appuyez sur M pour modifier", True, white)
                        modif_rect = modif_text.get_rect(center=(window_x / 2, window_y / 2))
                        start_text = small_font.render("Appuyez sur Entrée pour lancer le jeu", True, white)
                        start_rect = start_text.get_rect(center=(window_x / 2, window_y / 2 + 40))

                        game_window.blit(confirm_text, confirm_rect)
                        game_window.blit(modif_text, modif_rect)
                        game_window.blit(start_text, start_rect)

                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_m:
                                    pseudo = ""
                                    return display_intro()
                                if event.key == pygame.K_RETURN:
                                    game_loop()
                                    return

def reset_game():
    global pseudo
    pseudo = ""  # Réinitialiser le pseudo (ou d'autres variables si nécessaire)
    display_intro()

def menu():
    global paused, gameover, score

    my_font = pygame.font.SysFont('times new roman', 50)
    small_font = pygame.font.SysFont('times new roman', 30)

    if not gameover:
        menu_surface = my_font.render('Paused', True, red)
        resume_surface = small_font.render('Press ESC to resume', True, white)
        resume_rect = resume_surface.get_rect(center=(window_x / 2, window_y / 3 + 25))
    else:
        menu_surface = my_font.render('GAME OVER', True, red)
        save_score(score, pseudo)  # Sauvegarder le score lorsque le jeu est terminé

    menu_rect = menu_surface.get_rect(center=(window_x / 2, window_y / 8))

    score_surface = small_font.render('Score : ' + str(score), True, green)
    score_rect = score_surface.get_rect(center=(window_x / 2, window_y / 4))

    restart_surface = small_font.render('Press R to Restart', True, white)
    restart_rect = restart_surface.get_rect(center=(window_x / 2, window_y / 3 + 75))

    reset_surface = small_font.render('Press C to Reset Game', True, white)
    reset_rect = reset_surface.get_rect(center=(window_x / 2, window_y / 3 + 125))

    quit_surface = small_font.render('Press Q to Quit', True, white)
    quit_rect = quit_surface.get_rect(center=(window_x / 2, window_y / 3 + 175))

    while True:
        game_window.fill(black)
        if not gameover:
            game_window.blit(resume_surface, resume_rect)
        game_window.blit(menu_surface, menu_rect)
        game_window.blit(score_surface, score_rect)
        game_window.blit(restart_surface, restart_rect)
        game_window.blit(reset_surface, reset_rect)
        game_window.blit(quit_surface, quit_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_c:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_loop():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score, snake_speed, gameover, pseudo

    gameover = False
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    snake_speed = 7

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    menu()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10 or snake_position[1] < 0 or snake_position[1] > window_y - 10:
            gameover = True
            menu()

        if snake_position in snake_body[1:]:
            gameover = True
            menu()

        show_score(1, white, 'times new roman', 20)

        pygame.display.update()

        fps.tick(snake_speed)

if __name__ == "__main__":
    display_intro()


