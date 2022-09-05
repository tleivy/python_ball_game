import pygame

# constants
WINDOW_WIDTH = 700
WINDOW_LENGTH = 525
CENTER_X = 350
CENTER_Y = 212.5

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 242, 0)

IMAGE = './football_field.jpg'
LA_CUCARACHA = './la_cucaracha.mp3'
RADIUS = 60

MOUSE_LEFT = 1
MOUSE_SCROLL = 2
MOUSE_RIGHT = 3


def decide_ball_auto_movement(ball_pos_x, ball_pos_y, x_dir, y_dir):
    if ball_pos_x + RADIUS >= WINDOW_WIDTH:
        x_dir = -1
        ball_pos_x -= 7
    if ball_pos_y + RADIUS >= WINDOW_LENGTH:
        y_dir = -1
        ball_pos_y -= 7
    if ball_pos_x - RADIUS <= -60:
        x_dir = 1
        ball_pos_x += 7
    if ball_pos_y - RADIUS <= -60:
        y_dir = 1
        ball_pos_y += 7
    else:
        ball_pos_x += 3 * x_dir
        ball_pos_y += 3 * y_dir

    return ball_pos_x, ball_pos_y, x_dir, y_dir


def ball_auto_movement(clock, screen, background, player_image, ball_pos_x, ball_pos_y):
    refresh_rate = 60
    x_dir = 1
    y_dir = 1
    finish = False
    while not finish:
        # keeps the screen on until user quits it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        screen.blit(background, (0, 0))  # reload background

        # update ball position
        ball_pos_x, ball_pos_y, x_dir, y_dir = decide_ball_auto_movement(ball_pos_x, ball_pos_y, x_dir, y_dir)

        screen.blit(player_image, (ball_pos_x, ball_pos_y))
        pygame.display.flip()
        clock.tick(refresh_rate)

    pygame.quit()


def ball_user_movement(clock, screen, background, player_image):

    refresh_rate = 1000
    pygame.mouse.set_visible(False)  # mouse cursor invisible
    pygame.mixer.init()
    pygame.mixer.music.load(LA_CUCARACHA)

    finish = False
    mouse_pos_list = []
    while not finish:
        for event in pygame.event.get():

            # if user quits
            if event.type == pygame.QUIT:
                finish = True

            # if user presses mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT:
                    mouse_pos_list.append((pygame.mouse.get_pos()))
                elif event.button == MOUSE_RIGHT:
                    pygame.mixer.music.play()

            # if user presses keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mouse_pos_list = []

        screen.blit(background, (0, 0))  # reloading background

        # showing all mouse clicks of the user
        for pos in mouse_pos_list:
            screen.blit(player_image, pos)

        # mouse movement
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(player_image, mouse_pos)
        pygame.display.flip()
        clock.tick(refresh_rate)

    pygame.quit()


def init_game():
    pygame.init()

    game_type = input('select game type - auto or user (left button to keep ball location, space'
                      ' to clear all locations): ').lower()
    while game_type != 'auto' and game_type != 'user':
        game_type = input('select game type - auto or user (left button to keep ball location, space'
                          'to clear all locations): ').lower()

    # initializing screen
    size = (WINDOW_WIDTH, WINDOW_LENGTH)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")

    clock = pygame.time.Clock()  # initializing clock

    # loading pictures
    background = pygame.image.load(IMAGE)
    player_image = pygame.image.load('football_ball.png').convert()
    player_image.set_colorkey(YELLOW)  # ignore the background of the png
    screen.blit(background, (0, 0))  # loading background to screen from (0,0) - top left corner
    screen.blit(player_image, (CENTER_X, CENTER_Y))  # loading player image to middle of screen

    pygame.display.flip()  # updates the data of screen in video memory

    if game_type == 'auto':
        ball_auto_movement(clock, screen, background, player_image, ball_pos_x=CENTER_X, ball_pos_y=CENTER_Y)
    else:
        ball_user_movement(clock, screen, background, player_image)


def main():
    init_game()


if __name__ == '__main__':
    main()