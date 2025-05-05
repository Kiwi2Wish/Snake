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

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and len(pseudo) > 0:
            break  # sécurité en double pour bien sortir

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
