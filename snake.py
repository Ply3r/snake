import pygame
from colour import Color
from random import randint

# const, variables
WIDTH, HEIGHT = 800, 600
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
FPS = 30

pygame.font.init()
scoreText = pygame.font.SysFont('Comic Sans MS', 30)

WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Snake")

snake = [[200, 200], [220, 200]]

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
    for snake_pos in snake:
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


def move_snake(direction, velocity):
    if direction == 'RIGHT':
        snake.insert(0, [snake[0][0] + velocity, snake[0][1]])
    if direction == 'LEFT':
        snake.insert(0, [snake[0][0] - velocity, snake[0][1]])
    if direction == 'UP':
        snake.insert(0, [snake[0][0], snake[0][1] - velocity])
    if direction == 'DOWN':
        snake.insert(0, [snake[0][0], snake[0][1] + velocity])
    snake.pop()


def random_rgb(size):
    first_color = Color('#12c2e9')
    last_color = Color('#f64f59')
    arrayOfColors = list(first_color.range_to(last_color, size))
    hold = []
    for color in arrayOfColors:
        r = ((color.get_red() * 255) * 10) // 10
        g = ((color.get_green() * 255) * 10) // 10
        b = ((color.get_blue() * 255) * 10) // 10
        hold.append([r, g, b])
    return hold


def eat_apple(apple):
    x = snake[0][0]
    y = snake[0][1]
    if (x - 20 <= apple.x <= x + 20) and (y - 20 <= apple.y <= y + 20):
        snake.append([snake[-1][0], snake[-1][1]])
        return True
    return False


def draw_window(apple, score, game_over):
    if game_over:
        game_over_text = scoreText.render('Game Over', False, WHITE)
        WINDOW.fill([0, 0, 0])
        WINDOW.blit(game_over_text, [WIDTH//2 - 80, HEIGHT//2 - 40])
    else:
        scoreRender = scoreText.render(f'Score {score}', False, WHITE)

        WINDOW.fill([0, 0, 0])
        WINDOW.blit(scoreRender, [0, 0])
        WINDOW.blit(APPLE, [apple.x, apple.y])

        colors = random_rgb(len(snake))

        index = 0
        for pos in snake:
            SNAKE_SKIN = pygame.Surface((20, 20))
            SNAKE_SKIN.fill(colors[index])

            WINDOW.blit(SNAKE_SKIN, pos)
            index += 1


def check_body_colision():
    global score
    global game_over
    snake_head = snake[0]
    for index in range(len(snake)):
        print(snake_head, snake[index])
        if snake_head == snake[index] and index != 0:
            score = 0
            game_over = True


def check_game_over(game_over):
    snake_head = snake[0]
    global score
    if snake_head[0] <= -20 or snake_head[0] >= WIDTH + 20:
        game_over = True
        score = 0
    if snake_head[1] <= -20 or snake_head[1] >= HEIGHT + 20:
        game_over = True
        score = 0
    check_body_colision()
    return game_over


def restar_game(game_over):
    key_pressed = pygame.key.get_pressed()
    
    if key_pressed[pygame.K_r] and game_over:
        INITIAL_STATE = [[200, 200], [220, 200]]
        global snake
        snake = INITIAL_STATE
        game_over = False

    return game_over


direction = 'RIGHT'
score = 0
velocity = 20
game_over = False

def game_start():
    clock = pygame.time.Clock()

    apple_position = generate_position()
    apple = pygame.Rect(*apple_position, 20, 20)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        global direction
        global velocity
        global game_over
        global score

        direction = change_direction(direction)
        move_snake(direction, velocity)

        comeu = eat_apple(apple)
        if comeu:
            apple_position = generate_position()
            apple.x = apple_position[0]
            apple.y = apple_position[1]
            score += 1

        
        game_over = check_game_over(game_over)
        game_over = restar_game(game_over)

        draw_window(apple, score, game_over)
        pygame.display.update()



    pygame.quit()


game_start()
