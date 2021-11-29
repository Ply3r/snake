import pygame
from colour import Color
from random import randint

# const, variables
WIDTH, HEIGHT = 1240, 720
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
FPS = 30
SNAKE_COLORS = [['#12c2e9', '#f64f59'], ['#457fca', '#5691c8'], ['#00C9FF', '#92FE9D'], ['#f46b45', '#eea849'], ['#4158D0', '#FFCC70']]
snake_color = []

pygame.font.init()
title = pygame.font.SysFont('Arial', 50)
middleText = pygame.font.SysFont('Arial', 20)

WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Snake")

snake = [[200, 200], [220, 200]]

APPLE = pygame.Surface((20, 20))
APPLE.fill(RED)


def createBorder():
    border = []
    for index in range(0, WIDTH, 10):
        border.append([index, 0])

    for index in range(0, HEIGHT, 10):
        border.append([WIDTH - 10, index])

    for index in range(WIDTH, 0, -10):
        border.append([index, HEIGHT - 10])

    for index in range(HEIGHT, 0, -10):
        border.append([0, index])
    
    return border


border = createBorder()


def moveBorder():
    hold = border[-1]
    border.pop()
    border.insert(0, hold)


def pick_snake_color():
    global snake_color
    index = randint(0, len(SNAKE_COLORS) - 1)
    snake_color = SNAKE_COLORS[index]

pick_snake_color()


def create_apple():
    x = randint(20, WIDTH - 20)
    y = randint(20, HEIGHT - 20)
    return [x, y]


def generateGridPos(direction):
    hold = 0
    if (direction == 'x'): 
        hold = randint(10, WIDTH - 20)
    else:
        hold = randint(10, HEIGHT - 20)
        
    hold = (hold // 20) * 20

    if hold == 0:
        hold = 20
    

    return hold


def generate_position():
    x = generateGridPos('x')
    y = generateGridPos('y')
    position = [x, y]

    for pos in snake:
        if (pos[0] - 20 <= position[0] <= pos[0] + 20) \
                and (pos[1] - 20 <= position[1] <= pos[1] + 20):
            position = generate_position()
    
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


def random_rgb(size, color):
    first_color = Color(color[0])
    last_color = Color(color[1])
    arrayOfColors = list(first_color.range_to(last_color, size))
    hold = []
    for color in arrayOfColors:
        r = ((color.get_red() * 255) * 10) // 10
        g = ((color.get_green() * 255) * 10) // 10
        b = ((color.get_blue() * 255) * 10) // 10
        hold.append([r, g, b])
    return hold


def rgb_generator(color):
    first_color = Color(color[0])
    second_color = Color(color[1])
    first_array = list(first_color.range_to(second_color, len(border) //2))
    second_array = list(second_color.range_to(first_color, len(border) //2))
    array_of_colors = [*first_array, *second_array]
    hold = []
    for color in array_of_colors:
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
    scoreRender = middleText.render(f'Score {score}', False, WHITE)
    WINDOW.fill([0, 0, 0])

    if game_over:
        game_over_text = title.render('Game Over', False, WHITE)
        WINDOW.blit(game_over_text, [WIDTH//2 - 120, HEIGHT//2 - 80])
        WINDOW.blit(scoreRender, [WIDTH//2 - 30, HEIGHT//2])
    else:

        WINDOW.blit(scoreRender, [10, 10])
        WINDOW.blit(APPLE, [apple.x, apple.y])

        colors = random_rgb(len(snake), snake_color)

        index = 0
        for pos in snake:
            SNAKE_SKIN = pygame.Surface((20, 20))
            SNAKE_SKIN.fill(colors[index])

            WINDOW.blit(SNAKE_SKIN, pos)
            index += 1

        border_colors = rgb_generator(SNAKE_COLORS[0])
        border_index = 0
        for pos in border:
            BORDER_SKIN = pygame.Surface((10, 10))
            BORDER_SKIN.fill(border_colors[border_index])

            WINDOW.blit(BORDER_SKIN, pos)
            border_index += 1


def check_body_colision(game_over):
    snake_head = snake[0]
    for index in range(len(snake)):
        if snake_head == snake[index] and index != 0:
            game_over = True
    return game_over
            


def check_game_over(game_over):
    snake_head = snake[0]
    global velocity
    if snake_head[0] <= 0 or snake_head[0] >= WIDTH - 10:
        game_over = True
        
    if snake_head[1] <= 0 or snake_head[1] >= HEIGHT - 10:
        game_over = True
        
    game_over = check_body_colision(game_over)

    if game_over:
        velocity = 0
    return game_over


def restar_game(game_over):
    key_pressed = pygame.key.get_pressed()
    
    if key_pressed[pygame.K_r] and game_over:
        INITIAL_STATE = [[200, 200], [220, 200]]
        global snake
        global score
        global velocity
        pick_snake_color()
        velocity = 20
        score = 0
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
        moveBorder()

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
