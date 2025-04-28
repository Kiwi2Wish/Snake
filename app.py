
import pygame
import time
import random
import sys

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


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def menu():
    global paused, gameover

    my_font = pygame.font.SysFont('times new roman', 50)
    small_font = pygame.font.SysFont('times new roman', 30)

    if not gameover:
        menu_surface = my_font.render('Paused', True, red)

        resume_surface = small_font.render('Press ESC to resume', True, white)
        resume_rect = resume_surface.get_rect(center=(window_x / 2, window_y / 3+25))
    else:
        menu_surface = my_font.render('GAME OVER', True, red)

    menu_rect = menu_surface.get_rect(center=(window_x / 2, window_y / 8))

    score_surface = small_font.render('Score : ' + str(score), True, green)
    score_rect = score_surface.get_rect(center=(window_x / 2, window_y / 4))

    restart_surface = small_font.render('Press R to Restart', True, white)
    restart_rect = restart_surface.get_rect(center=(window_x / 2, window_y / 3+75))

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
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    game_loop()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_loop():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score, snake_speed, gameover

    gameover = False
    snake_position = [100, 50]
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
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
            snake_speed += 2
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))


        if (snake_position[0] < 0 or snake_position[0] > window_x - 10 or
            snake_position[1] < 0 or snake_position[1] > window_y - 10):
            gameover = True
            menu()
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                gameover = True
                menu()

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

game_loop()
