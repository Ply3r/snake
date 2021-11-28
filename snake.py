import pygame
from colour import Color
from random import randint

# const, variables
WIDTH, HEIGHT = 800, 600
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
FPS = 30
VELOCITY = 20

pygame.font.init()
scoreText = pygame.font.SysFont('Comic Sans MS', 30)

WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Snake")

SNAKE = [[200, 200], [220, 200]]

APPLE = pygame.Surface((20, 20))
APPLE.fill(RED)


def create_apple():
    x = randint(20, WIDTH - 20)
    y = randint(20, HEIGHT - 20)
    return [x, y]


def generate_position():
    x = randint(0, WIDTH - 40)
    y = randint(0, HEIGHT - 40)
    position = [x, y]
    for snake_pos in SNAKE:
        if (snake_pos[0] - 20 <= position[0] <= snake_pos[0] + 20) \
                and (snake_pos[1] - 20 <= position[1] <= snake_pos[1] + 20):
            generate_position()
    return position


def change_direction(direction):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'
    if key_pressed[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if key_pressed[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if key_pressed[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'
    return direction


def move_snake(direction):
    if direction == 'RIGHT':
        SNAKE.insert(0, [SNAKE[0][0] + VELOCITY, SNAKE[0][1]])
    if direction == 'LEFT':
        SNAKE.insert(0, [SNAKE[0][0] - VELOCITY, SNAKE[0][1]])
    if direction == 'UP':
        SNAKE.insert(0, [SNAKE[0][0], SNAKE[0][1] - VELOCITY])
    if direction == 'DOWN':
        SNAKE.insert(0, [SNAKE[0][0], SNAKE[0][1] + VELOCITY])
    SNAKE.pop()


def random_rgb(size):
    first_color = Color('#fc00ff')
    last_colot = Color('#00dbde')


def eat_apple(apple):
    x = SNAKE[0][0]
    y = SNAKE[0][1]
    if (x - 20 <= apple.x <= x + 20) and (y - 20 <= apple.y <= y + 20):
        SNAKE.append([SNAKE[-1][0] + 20, SNAKE[-1][1]])
        return True
    return False


def draw_window(apple, score):
    scoreRender = scoreText.render(f'Score {score}', False, WHITE)

    WINDOW.fill([0, 0, 0])
    WINDOW.blit(scoreRender, [0, 0])
    WINDOW.blit(APPLE, [apple.x, apple.y])

    colors = random_rgb(len(SNAKE))

    index = 0
    for pos in SNAKE:
        SNAKE_SKIN = pygame.Surface((20, 20))
        SNAKE_SKIN.fill(colors[index])

        WINDOW.blit(SNAKE_SKIN, pos)
        index += 1


def game_start():
    clock = pygame.time.Clock()

    apple_position = generate_position()
    apple = pygame.Rect(*apple_position, 20, 20)

    direction = 'RIGHT'
    score = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        direction = change_direction(direction)
        move_snake(direction)

        comeu = eat_apple(apple)
        if comeu:
            apple_position = generate_position()
            apple.x = apple_position[0]
            apple.y = apple_position[1]
            score += 1

        draw_window(apple, score)
        pygame.display.update()



    pygame.quit()


game_start()
