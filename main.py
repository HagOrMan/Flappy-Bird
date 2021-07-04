import random
import pygame
import sys

pygame.init()

# Sets up window.
win_width = 1000
win_height = 600
win_colour = (0, 0, 0)
WIN = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")
game_over1 = False
game_over2 = False
counting_down = False
choosing_char = False
choosing_char2 = False
choosing_mode = True
solo_game = True
score = 0
score2 = 0
choice1 = 0
choice2 = 0
p1_wins = 0
p2_wins = 0
p1_wins_base = 0
p2_wins_base = 0

# Each different type of bird.
main_bird_img = pygame.image.load('flappy_bird.png')
main_bird_jump = pygame.image.load('flappy_bird_jump.png')
main_bird_fall = pygame.image.load('flappy_bird_fall.png')

purp_bird_img = pygame.image.load('flappy_bird_purple.png')
purp_bird_jump = pygame.image.load('purp_bird_jump.png')
purp_bird_fall = pygame.image.load('purp_bird_fall.png')

blue_bird_img = pygame.image.load('flappy_bird_blue.png')
blue_bird_jump = pygame.image.load('blue_bird_jump.png')
blue_bird_fall = pygame.image.load('blue_bird_fall.png')

green_bird_img = pygame.image.load('flappy_bird_green.png')
green_bird_jump = pygame.image.load('green_bird_jump.png')
green_bird_fall = pygame.image.load('green_bird_fall.png')

# Variables for the bird.
bird_img = pygame.image.load('flappy_bird.png')
bird_jump = pygame.image.load('flappy_bird_jump.png')
bird_fall = pygame.image.load('flappy_bird_fall.png')
bird_img2 = pygame.image.load('flappy_bird.png')
bird_jump2 = pygame.image.load('flappy_bird_jump.png')
bird_fall2 = pygame.image.load('flappy_bird_fall.png')

bird = main_bird_img
bird2 = main_bird_img
bird_x = 100
bird_y = int(win_height / 2 - 100)
bird_x2 = 100
bird_y2 = int(win_height / 2 - 100)

jump_speed = 8.5
fall_speed = 3
fall_time = 0
jump_num = 0
has_jumped = False
fall_time2 = 0
jump_num2 = 0
has_jumped2 = False

# Dict of all birds for easy access.
birds = {1: (main_bird_img, main_bird_jump, main_bird_fall), 2: (purp_bird_img, purp_bird_jump, purp_bird_fall),
         3: (blue_bird_img, blue_bird_jump, blue_bird_fall), 4: (green_bird_img, green_bird_jump, green_bird_fall)}

clock = pygame.time.Clock()

# Variables for pipe.
gap = 250
pipe_col = (255, 20, 20)
pipe_width = 80
pipe_speed = 4
pipe1 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, win_height - 60, pipe_width, 60))
pipe2 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, 0, pipe_width, win_height - gap - pipe1.height))
wait_time = 3000

# List of all pipes on screen.
pipes = [pipe1, pipe2]


# Resets the game.
def reset_game():

    global game_over1, bird, bird_y, fall_time, jump_num, has_jumped, pipes, wait_time, score, fall_time2, jump_num2
    global has_jumped2, bird_y2, bird2, score2, game_over2, p1_wins, p2_wins, bird_x, bird_x2, counting_down

    score = 0
    score2 = 0

    bird = bird_img
    bird2 = bird_img2
    bird_y = int(win_height / 2 - 120)
    bird_y2 = int(win_height / 2 - 100)
    bird_x = 100
    bird_x2 = 100
    fall_time = 0
    jump_num = 0
    has_jumped = False
    fall_time2 = 0
    jump_num2 = 0
    has_jumped2 = False

    # Resets the pipes.
    reset_pipe1 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, win_height - 60, pipe_width, 60))
    reset_pipe2 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, 0,
                                                   pipe_width, win_height - gap - pipe1.height))
    pipes = [reset_pipe1, reset_pipe2]
    wait_time = 3000

    p1_wins = p1_wins_base
    p2_wins = p2_wins_base

    game_over1 = False
    game_over2 = False
    counting_down = True


# Draws everything on the board.
def draw_game():

    global pipes, bird_x, bird_x2

    WIN.fill(win_colour)

    # Draws the solo bird if it is a solo game.
    if solo_game and not game_over1:

        # Adds the bird to the window.
        WIN.blit(bird, (bird_x, bird_y))

        # Deletes any pipes from the list that are off the screen.
        pipes[:] = [pipes[y] for y in range(len(pipes)) if pipes[y].x + pipes[y].width >= 0]

        # Draws all the pipes on the screen and moves them too.
        for item in range(len(pipes)):
            pipes[item].x -= pipe_speed
            pygame.draw.rect(WIN, pipe_col, pipes[item])

    # Draws both birds if it is a duel.
    elif (not solo_game) and not (game_over1 and game_over2):

        # Adds the birds to the window.
        WIN.blit(bird, (bird_x, bird_y))
        WIN.blit(bird2, (bird_x2, bird_y2))

        # Makes a dead bird move out of the screen.
        if game_over1 and bird_x > -100:
            bird_x -= pipe_speed
        elif game_over2 and bird_x2 > -100:
            bird_x2 -= pipe_speed

        # Deletes any pipes from the list that are off the screen.
        pipes[:] = [pipes[y] for y in range(len(pipes)) if pipes[y].x + pipes[y].width >= 0]

        # Draws all the pipes on the screen and moves them too.
        for item in range(len(pipes)):
            pipes[item].x -= pipe_speed
            pygame.draw.rect(WIN, pipe_col, pipes[item])

    # Draws a game over sign if the game is over.
    else:
        draw_game_over()

    # Shows the score of each player.
    score_font = pygame.font.SysFont('timesnewroman', 60)
    player_font = pygame.font.SysFont('timesnewroman', 30)

    # Adds a certain value to the horizontal placement of the score if it is a solo game.
    solo_mod = 0
    if solo_game:
        solo_mod = 100

    # Only says player 1 if they are facing someone else.
    if not solo_game:
        player_txt = player_font.render('Player 1', False, (0, 255, 255))
        WIN.blit(player_txt, (win_width / 2 - 140, 5))

        score_txt2 = score_font.render(str(score2), False, (0, 255, 255))
        player_txt2 = player_font.render('Player 2', False, (0, 255, 255))
        WIN.blit(score_txt2, (win_width / 2 + 75, 35))
        WIN.blit(player_txt2, (win_width / 2 + 40, 5))

    score_txt = score_font.render(str(score), False, (0, 255, 255))
    WIN.blit(score_txt, (win_width / 2 - 110 + solo_mod, 35))


# Returns if the bird collided with any of the pipes.
def collision():

    # Goes through the pipes and checks the ones which are in the x coordinate range of the bird.
    for item in pipes:
        if 190 >= item.x >= 50:

            # Checks if the bird collided.
            if (item.y <= bird_y <= item.y + item.height or
                    item.y <= bird_y + 55 <= item.y + item.height):
                return True


# Returns if the second bird collided with any of the pipes.
def collision2():

    # Goes through the pipes and checks the ones which are in the x coordinate range of the bird.
    for item in pipes:
        if 190 >= item.x >= 50:

            # Checks if the bird collided.
            if (item.y <= bird_y2 <= item.y + item.height or
                    item.y <= bird_y2 + 55 <= item.y + item.height):
                return True


# Shows that the game is over.
def draw_game_over():

    global p1_wins_base, p2_wins_base

    # Draws the basic game over notifications.
    game_over_font = pygame.font.SysFont('timesnewroman', 36)
    restart_font = pygame.font.SysFont('timesnewroman', 26)
    winner_txt = ''
    winner_gap = win_width / 2 - 210

    # Displays a winner if they are playing a duel game.
    if not solo_game:
        if score < score2:
            winner_txt = ' Player 2 Wins!'
            p2_wins_base = p2_wins + 1
        elif score > score2:
            winner_txt = ' Player 1 Wins!'
            p1_wins_base = p1_wins + 1
        else:
            winner_txt = ' It\'s a tie!'
            winner_gap = win_width / 2 - 175
    else:
        winner_txt = ' Your score is {}!'.format(str(score))
    game_over_txt = game_over_font.render('Game Over!' + winner_txt, False, (255, 255, 255))
    restart_txt = restart_font.render(str('Click anywhere to restart'), False, (255, 255, 255))
    choose_txt = restart_font.render(str('Press \'C\' to choose another character'), False, (255, 255, 255))
    mode_txt = restart_font.render(str('Press \'X\' to choose another game mode'), False, (255, 255, 255))
    WIN.blit(game_over_txt, (winner_gap, win_height / 2 - 50))
    WIN.blit(restart_txt, (win_width / 2 - 150, win_height / 2 - 10))
    WIN.blit(choose_txt, (win_width / 2 - 210, win_height / 2 + 20))
    WIN.blit(mode_txt, (win_width / 2 - 220, win_height / 2 + 50))

    # Shows how many wins each player has.
    if not solo_game:
        p1_win_txt = restart_font.render('P1 Wins: ' + str(p1_wins_base), False, (255, 255, 255))
        p2_win_txt = restart_font.render('P2 Wins: ' + str(p2_wins_base), False, (255, 255, 255))
        WIN.blit(p1_win_txt, (20, win_height - 150))
        WIN.blit(p2_win_txt, (win_width - 150, win_height - 150))


# Increments the score when the user passes a pipe.
def add_score():

    global score, score2

    # Goes through the pipes and checks the ones which are just past the x coordinate of the bird.
    for item in pipes:
        if item.x == 52:
            if not game_over1:
                score += 0.5
            if not game_over2:
                score2 += 0.5

    score = int(score)
    score2 = int(score2)


# Lets the user choose which character to use.
def choose_chars():

    # Shows all bird options.
    WIN.fill(win_colour)
    WIN.blit(pygame.image.load('big_bird_main.png'), (0, 0))
    WIN.blit(pygame.image.load('big_bird_purple.png'), (win_width // 2, 0))
    WIN.blit(pygame.image.load('big_bird_blue.png'), (0, win_height // 2))
    WIN.blit(pygame.image.load('big_bird_green.png'), (win_width // 2, win_height // 2))

    if not choosing_char:
        choosing_font = pygame.font.SysFont('timesnewroman', 26)
        choosing_txt = choosing_font.render('1', False, (255, 255, 255))
        if choice1 < 3:
            WIN.blit(choosing_txt, (int(choice1 - 0.5) * win_width // 2 + 20, 20))
        else:
            WIN.blit(choosing_txt, (int(choice1 - 2.5) * win_width // 2 + 20, win_height // 2 + 20))


# Gets the user's choice on which bird they are playing as.
def get_choice(posit):
    x, y = posit
    rows = y // (win_height / 2)
    cols = x // (win_width / 2)
    return int(rows * 2), int(cols + 1)


# Lets the user choose if they want to play solo or double.
def choose_mode():

    WIN.fill(win_colour)

    # Shows text for game modes.
    choosing_font_top = pygame.font.SysFont('timesnewroman', 40)
    choose_msg = choosing_font_top.render('Choose your game mode', False, (255, 255, 255))

    choosing_font = pygame.font.SysFont('timesnewroman', 32)
    choose_solo = choosing_font.render('Solo', False, (255, 255, 255))
    choose_duel = choosing_font.render('Play against a friend', False, (255, 255, 255))

    WIN.blit(choose_msg, (win_width // 2 - 200, 20))
    WIN.blit(choose_solo, (win_width // 2 - 255, win_height // 2 - 100))
    WIN.blit(choose_duel, (win_width // 2 + 105, win_height // 2 - 100))

    # Tells the user the controls for the game
    p1_control_txt = choosing_font.render('P1: Press SPACE to jump!', False, (255, 255, 255))
    p2_control_txt = choosing_font.render('P2: Press M to jump!', False, (255, 255, 255))
    WIN.blit(p1_control_txt, (win_width // 2 - 390, win_height // 2 + 100))
    WIN.blit(p2_control_txt, (win_width // 2 + 90, win_height // 2 + 100))

    # Draws a surrounding outline for the choices.
    pygame.draw.rect(WIN, (255, 255, 255), [win_width // 2 - 375, win_height // 2 - 130, 300, 100], 2)
    pygame.draw.rect(WIN, (255, 255, 255), [win_width // 2 + 60, win_height // 2 - 130, 350, 100], 2)

    # Shows birds under text to represent the number of players in each game mode.
    WIN.blit(main_bird_img, (win_width // 2 - 270, win_height // 2))
    WIN.blit(main_bird_img, (win_width // 2 + 100, win_height // 2))
    WIN.blit(purp_bird_img, (win_width // 2 + 250, win_height // 2))

    pygame.display.flip()


# Counts down before restarting the game.
def count_down():
    count_font = pygame.font.SysFont('timesnewroman', 60)
    counter = 3
    # Waits 1 second before displaying each item.
    while counter > 0:
        WIN.fill(win_colour)
        count_txt = count_font.render(str(counter), False, (255, 255, 255))
        WIN.blit(count_txt, (win_width // 2 - 20, win_height // 2 - 40))
        pygame.display.flip()
        pygame.time.delay(1000)
        counter -= 1
    global counting_down
    counting_down = False


while True:

    clock.tick(50)
    keysPressed = pygame.key.get_pressed()

    # Whenever a button is clicked or mouse pressed.
    for event in pygame.event.get():

        # When the user exits the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # If player 1 jumps.
        elif keysPressed[pygame.K_SPACE]:

            if not game_over1:
                if not has_jumped:

                    # Sets has_jumped to true and resets fall time.
                    has_jumped = True
                    fall_time = 0
                    bird = bird_jump
                else:
                    jump_num = 0

        # If player 2 jumps.
        elif keysPressed[pygame.K_m]:

            if not game_over2:
                if not has_jumped2:

                    # Sets has_jumped2 to true and resets fall time.
                    has_jumped2 = True
                    fall_time2 = 0
                    bird2 = bird_jump2

                else:
                    jump_num2 = 0

        # Resets the game when they click.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # If they are choosing which mode to play, uses the position of the click to see if a mode was chosen.
            if choosing_mode:
                x, y = pos
                if win_width // 2 - 375 <= x <= win_width // 2 - 75 and win_height // 2 - 130 <= y <= win_height // 2 - 30:
                    solo_game = True
                    choosing_mode = False
                    choosing_char = True
                elif win_width // 2 + 60 <= x <= win_width // 2 + 410 and win_height // 2 - 130 <= y <= win_height // 2 - 30:
                    solo_game = False
                    choosing_mode = False
                    choosing_char = True
                    choosing_char2 = True

            # If they are doing a duel game and choosing their character, lets both players choose.
            elif (not solo_game) and (choosing_char or choosing_char2):
                if choosing_char:
                    row, col = get_choice(pos)
                    choice1 = row + col
                    bird_img, bird_jump, bird_fall = birds[choice1]
                    choosing_char = False
                elif choosing_char2:
                    row, col = get_choice(pos)
                    choice2 = row + col
                    if choice1 != choice2:
                        bird_img2, bird_jump2, bird_fall2 = birds[choice2]
                        choosing_char2 = False
                        reset_game()

            # Lets the solo player choose another character.
            elif solo_game and choosing_char:
                row, col = get_choice(pos)
                choice1 = row + col
                bird_img, bird_jump, bird_fall = birds[choice1]
                choosing_char = False
                reset_game()

            # Restarts the game as long as all the people playing have finished.
            elif ((not solo_game) and game_over1 and game_over2) or (solo_game and game_over1):
                reset_game()

        # Lets them choose another character.
        elif keysPressed[pygame.K_c]:
            if ((not solo_game) and game_over1 and game_over2) or (solo_game and game_over1):
                choosing_char = True
                choosing_char2 = True

        # Lets them choose a different game mode.
        elif keysPressed[pygame.K_x]:
            if ((not solo_game) and game_over1 and game_over2) or (solo_game and game_over1):
                choosing_mode = True

    # If they are choosing which mode to play, brings up that screen.
    if choosing_mode:
        choose_mode()

    # Counts down before starting the game.
    elif counting_down:
        count_down()

    # If they are not choosing their mode and are done choosing characters, lets them play.
    elif (not solo_game) and not (choosing_char or choosing_char2):

        # Increments the score as long as the game is not over
        if not (game_over1 and game_over2):
            add_score()

            # Makes pipes every so often, making more as the game goes on.
            wait_time -= 20
            if score > 5:
                wait_time -= 2
            if score > 10:
                wait_time -= 2
            if score > 15:
                wait_time -= 2
            if score > 20:
                wait_time -= 2
            if score > 25:
                wait_time -= 2

            # Adds new pipes, both the top and bottom, when the wait timer reaches 0.
            if wait_time <= 0:
                wait_time = 3000
                pipe_height = random.randrange(50, 400, 50)
                new_pipe1 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, win_height - pipe_height,
                                                             pipe_width, pipe_height))
                new_pipe2 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, 0,
                                                             pipe_width, win_height - gap - pipe_height))
                pipes.append(new_pipe1)
                pipes.append(new_pipe2)

        # Stops player 1 from falling or jumping if they crashed.
        if not game_over1:

            # Adjusts the gap between pipes depending on the score.
            if score == 10:
                gap = 230
            if score == 15:
                gap = 210
            if score == 20:
                gap = 200

            # Mechanics for if they are jumping or falling.
            if has_jumped:

                # Increases the jump number as long as it is less than 12 and changes the y position.
                if jump_num < 12:
                    jump_num += 1

                # Checks if the bird will hit the ceiling and ends to game if so, if not letting it move.
                if bird_y - jump_speed >= -18:
                    bird_y -= jump_speed
                else:
                    bird_y = 0
                    game_over1 = True

                # If they are at 12, the top of the jump, resets the variables.
                if jump_num == 12:
                    jump_num = 0
                    has_jumped = False

            # If they are falling.
            else:

                # Checks if the bird will be falling and hitting the floor.
                if bird_y + fall_speed ** (1.2 + fall_time * 0.1) < win_height - 71:
                    bird_y += fall_speed ** (1.2 + fall_time * 0.1)

                    # Increments fall time, and if it is high enough, the bird looks like it is falling.
                    fall_time += 0.35
                    if fall_time > 8:
                        bird = bird_fall
                    else:
                        bird = bird_img

                else:
                    # The bird has fallen to the ground so the game is over and the height is set to make it look real.
                    bird_y = win_height - 57
                    game_over1 = True

            # Now that they have fallen/jumped, checks if they collided with anything and ends the game if so.
            if collision():
                game_over1 = True

        # Stops player 2 from falling or jumping if they crashed.
        if not game_over2:

            # Adjusts the gap between pipes depending on the score.
            if score2 == 10:
                gap = 230
            if score2 == 15:
                gap = 210
            if score2 == 20:
                gap = 200

            # Mechanics for if they are jumping or falling.
            if has_jumped2:

                # Increases the jump number as long as it is less than 12 and changes the y position.
                if jump_num2 < 12:
                    jump_num2 += 1

                # Checks if the bird will hit the ceiling and ends to game if so, if not letting it move.
                if bird_y2 - jump_speed >= -18:
                    bird_y2 -= jump_speed
                else:
                    bird_y2 = 0
                    game_over2 = True

                # If they are at 12, the top of the jump, resets the variables.
                if jump_num2 == 12:
                    jump_num2 = 0
                    has_jumped2 = False

            # If they are falling.
            else:

                # Checks if the bird will be falling and hitting the floor.
                if bird_y2 + fall_speed ** (1.2 + fall_time2 * 0.1) < win_height - 71:
                    bird_y2 += fall_speed ** (1.2 + fall_time2 * 0.1)

                    # Increments fall time, and if it is high enough, the bird looks like it is falling.
                    fall_time2 += 0.35
                    if fall_time2 > 8:
                        bird2 = bird_fall2
                    else:
                        bird2 = bird_img2

                else:
                    # The bird has fallen to the ground so the game is over and the height is set to make it look real.
                    bird_y2 = win_height - 57
                    game_over2 = True

            # Now that they have fallen/jumped, checks if they collided with anything and ends the game if so.
            if collision2():
                game_over2 = True

        if not counting_down:
            draw_game()

    # If they are playing solo and done choosing, lets them play.
    elif solo_game and not choosing_char:

        # Stops player 1 from falling or jumping if they crashed.
        if not game_over1:

            add_score()

            # Makes pipes every so often, making more as the game goes on.
            wait_time -= 20
            if score > 5:
                wait_time -= 2
            if score > 10:
                wait_time -= 2
            if score > 15:
                wait_time -= 2
            if score > 20:
                wait_time -= 2
            if score > 25:
                wait_time -= 2

            # Adds new pipes, both the top and bottom, when the wait timer reaches 0.
            if wait_time <= 0:
                wait_time = 3000
                pipe_height = random.randrange(50, 400, 50)
                new_pipe1 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, win_height - pipe_height,
                                                             pipe_width, pipe_height))
                new_pipe2 = pygame.draw.rect(WIN, pipe_col, (win_width - pipe_width, 0,
                                                             pipe_width, win_height - gap - pipe_height))
                pipes.append(new_pipe1)
                pipes.append(new_pipe2)

            # Adjusts the gap between pipes depending on the score.
            if score == 10:
                gap = 230
            if score == 15:
                gap = 210
            if score == 20:
                gap = 200

            # Mechanics for if they are jumping or falling.
            if has_jumped:

                # Increases the jump number as long as it is less than 12 and changes the y position.
                if jump_num < 12:
                    jump_num += 1

                # Checks if the bird will hit the ceiling and ends to game if so, if not letting it move.
                if bird_y - jump_speed >= -18:
                    bird_y -= jump_speed
                else:
                    bird_y = 0
                    game_over1 = True

                # If they are at 12, the top of the jump, resets the variables.
                if jump_num == 12:
                    jump_num = 0
                    has_jumped = False

            # If they are falling.
            else:

                # Checks if the bird will be falling and hitting the floor.
                if bird_y + fall_speed ** (1.2 + fall_time * 0.1) < win_height - 71:
                    bird_y += fall_speed ** (1.2 + fall_time * 0.1)

                    # Increments fall time, and if it is high enough, the bird looks like it is falling.
                    fall_time += 0.35
                    if fall_time > 8:
                        bird = bird_fall
                    else:
                        bird = bird_img

                else:
                    # The bird has fallen to the ground so the game is over and the height is set to make it look real.
                    bird_y = win_height - 57
                    game_over1 = True

            # Now that they have fallen/jumped, checks if they collided with anything and ends the game if so.
            if collision():
                game_over1 = True

        if not counting_down:
            draw_game()

    else:
        choose_chars()

    pygame.display.flip()
