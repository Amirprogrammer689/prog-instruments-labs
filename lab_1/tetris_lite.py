import pygame as pg
import random
import time
import sys
from pygame.locals import *


FPS = 25
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
BLOCK_SIZE, CUP_HEIGHT, CUP_WIDTH = 20, 20, 10

SIDE_FREQ, DOWN_FREQ = 0.15, 0.1 # передвижение в сторону и вниз

SIDE_MARGIN = int((WINDOW_WIDTH - CUP_WIDTH * BLOCK_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (CUP_HEIGHT * BLOCK_SIZE) - 5

COLORS = (
    (0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0)
) # синий, зеленый, красный, желтый
LIGHT_COLORS = (
    (30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30)
) # светло-синий, светло-зеленый, светло-красный, светло-желтый

WHITE, GRAY, BLACK  = (255, 255, 255), (185, 185, 185), (0, 0, 0)
BRD_COLOR, BG_COLOR, TXT_COLOR, TITLE_COLOR, INFO_COLOR = WHITE, GRAY, BLACK, COLORS[3], COLORS[0]

FIG_WIDTH, FIG_HEIGHT = 5, 5
EMPTY = 'o'

FIGURES = {
    'S': [
        ['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'],
        ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']
    ],
    'Z': [
        ['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'],
        ['ooooo', 'ooxoo', 'oxxoo', 'oxooo', 'ooooo']
    ],
    'J': [
        ['ooooo', 'oxooo', 'oxxxo', 'ooooo', 'ooooo'],
        ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
        ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'],
        ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']
    ],
    'L': [
        ['ooooo', 'oooxo', 'oxxxo', 'ooooo', 'ooooo'],
        ['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
        ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo'],
        ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo']
    ],
    'I': [
        ['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'],
        ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']
    ],
    'O': [
        ['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']
    ],
    'T': [
        ['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'],
        ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
        ['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'],
        ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']
    ]
}


def pause_screen():
    pause_surface = pg.Surface((600, 500), pg.SRCALPHA)
    pause_surface.fill((0, 0, 255, 127))
    display_surface.blit(pause_surface, (0, 0))


def main():
    global fps_clock, display_surface, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Тетрис Lite')
    show_text('Тетрис Lite')

    while True: # начинаем игру
        run_tetris()
        pause_screen()
        show_text('Игра закончена')


def run_tetris():
    cup = empty_cup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calc_speed(points)
    falling_figure = get_new_figure()
    next_figure = get_new_figure()

    while True:
        if falling_figure == None:
            # если нет падающих фигур, генерируем новую
            falling_figure = next_figure
            next_figure = get_new_figure()
            last_fall = time.time()

            if not check_position(cup, falling_figure):
                return # если на игровом поле нет свободного места - игра закончена

        quit_game()

        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause_screen()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and check_position(cup, falling_figure, adj_x=-1):
                    falling_figure['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and check_position(cup, falling_figure, adj_x=1):
                    falling_figure['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    falling_figure['rotation'] = (
                                                         falling_figure['rotation'] + 1
                                                 ) % len(FIGURES[falling_figure['shape']])
                    if not check_position(cup, falling_figure):
                        falling_figure['rotation'] = (
                                                             falling_figure['rotation'] - 1
                                                     ) % len(FIGURES[falling_figure['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if check_position(cup, falling_figure, adj_y=1):
                        falling_figure['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, CUP_HEIGHT):
                        if not check_position(cup, falling_figure, adj_y=i):
                            break
                    falling_figure['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > SIDE_FREQ:
            if going_left and check_position(cup, falling_figure, adj_x=-1):
                falling_figure['x'] -= 1
            elif going_right and check_position(cup, falling_figure, adj_x=1):
                falling_figure['x'] += 1
            last_side_move = time.time()

        if (going_down and
                time.time() - last_move_down > DOWN_FREQ
                and check_position(cup, falling_figure, adj_y=1)):
            falling_figure['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed: # свободное падение фигуры
            if not check_position(cup, falling_figure, adj_y=1): # проверка "приземления" фигуры
                add_to_cup(cup, falling_figure) # фигура приземлилась, добавляем ее в содержимое стакана
                points += clear_completed(cup)
                level, fall_speed = calc_speed(points)
                falling_figure = None
            else: # фигура пока не приземлилась, продолжаем движение вниз
                falling_figure['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surface.fill(BG_COLOR)
        draw_title()
        game_cup(cup)
        draw_info(points, level)
        draw_next_figure(next_figure)
        if falling_figure != None:
            draw_figure(falling_figure)
        pg.display.update()
        fps_clock.tick(FPS)


def txt_objects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop_game():
    pg.quit()
    sys.exit()


def check_keys():
    quit_game()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key

    return None


def show_text(text):
    title_surf, title_rect = txt_objects(text, big_font, TITLE_COLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2) - 3,
                         int(WINDOW_HEIGHT / 2) - 3)
    display_surface.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = txt_objects(
        'Нажмите любую клавишу для продолжения',
        basic_font, TITLE_COLOR
    )
    press_key_rect.center = (int(WINDOW_WIDTH / 2),
                             int(WINDOW_HEIGHT / 2) + 100)
    display_surface.blit(press_key_surf, press_key_rect)

    while check_keys() == None:
        pg.display.update()
        fps_clock.tick()


def quit_game():
    for event in pg.event.get(QUIT): # проверка всех событий, приводящих к выходу из игры
        stop_game()

    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop_game()
        pg.event.post(event)


def calc_speed(points):
    # вычисляет уровень
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def get_new_figure():
    # возвращает новую фигуру со случайным цветом и углом поворота
    shape = random.choice(list(FIGURES.keys()))
    new_figure = {
        'shape': shape,
        'rotation': random.randint(0, len(FIGURES[shape]) - 1),
        'x': int(CUP_WIDTH / 2) - int(FIG_WIDTH / 2),
        'y': -2,
        'color': random.randint(0, len(COLORS)-1)
    }
    return new_figure


def add_to_cup(cup, fig):
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            if FIGURES[fig['shape']][fig['rotation']][y][x] != EMPTY:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def empty_cup():
    # создает пустой стакан
    cup = []
    for i in range(CUP_WIDTH):
        cup.append([EMPTY] * CUP_HEIGHT)
    return cup


def in_cup(x, y):
    return x >= 0 and x < CUP_WIDTH and y < CUP_HEIGHT


def check_position(cup, fig, adj_x=0, adj_y=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            above_cup = y + fig['y'] + adj_y < 0
            if above_cup or FIGURES[fig['shape']][fig['rotation']][y][x] == EMPTY:
                continue
            if not in_cup(x + fig['x'] + adj_x, y + fig['y'] + adj_y):
                return False
            if cup[x + fig['x'] + adj_x][y + fig['y'] + adj_y] != EMPTY:
                return False
    return True


def is_completed(cup, y):
    # проверяем наличие полностью заполненных рядов
    for x in range(CUP_WIDTH):
        if cup[x][y] == EMPTY:
            return False
    return True


def clear_completed(cup):
    # Удаление заполенных рядов и сдвиг верхних рядов вниз
    removed_lines = 0
    y = CUP_HEIGHT - 1

    while y >= 0:
        if is_completed(cup, y):
           for push_down_y in range(y, 0, -1):
                for x in range(CUP_WIDTH):
                    cup[x][push_down_y] = cup[x][push_down_y-1]
           for x in range(CUP_WIDTH):
                cup[x][0] = EMPTY
           removed_lines += 1
        else:
            y -= 1

    return removed_lines


def convert_coords(block_x, block_y):
    return (SIDE_MARGIN + (block_x * BLOCK_SIZE)), (TOP_MARGIN + (block_y * BLOCK_SIZE))


def draw_block(block_x, block_y, color, pixel_x=None, pixel_y=None):
    #отрисовка квадратных блоков, из которых состоят фигуры
    if color == EMPTY:
        return

    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convert_coords(block_x, block_y)

    pg.draw.rect(display_surface, COLORS[color],
                 (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 1,
                  BLOCK_SIZE - 1), 0, 3)
    pg.draw.rect(display_surface, LIGHT_COLORS[color],
                 (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 4,
                  BLOCK_SIZE - 4), 0, 3)
    pg.draw.circle(display_surface, COLORS[color],
                   (pixel_x + BLOCK_SIZE / 2, pixel_y + BLOCK_SIZE / 2), 5)


def game_cup(cup):
    # граница игрового поля-стакана
    pg.draw.rect(display_surface, BRD_COLOR,
                 (SIDE_MARGIN - 4, TOP_MARGIN - 4,
                  (CUP_WIDTH * BLOCK_SIZE) + 8,
                  (CUP_HEIGHT * BLOCK_SIZE) + 8), 5)

    # фон игрового поля
    pg.draw.rect(display_surface, BG_COLOR,
                 (SIDE_MARGIN, TOP_MARGIN,
                  BLOCK_SIZE * CUP_WIDTH,
                  BLOCK_SIZE * CUP_HEIGHT))

    for x in range(CUP_WIDTH):
        for y in range(CUP_HEIGHT):
            draw_block(x, y, cup[x][y])


def draw_title():
    title_surf = big_font.render('Тетрис Lite', True, TITLE_COLOR)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (WINDOW_WIDTH - 425, 30)
    display_surface.blit(title_surf, title_rect)


def draw_info(points, level):
    points_surf = basic_font.render(f'Баллы: {points}', True, TXT_COLOR)
    points_rect = points_surf.get_rect()
    points_rect.topleft = (WINDOW_WIDTH - 550, 180)
    display_surface.blit(points_surf, points_rect)

    level_surf = basic_font.render(f'Уровень: {level}', True, TXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOW_WIDTH - 550, 250)
    display_surface.blit(level_surf, level_rect)

    pause_surf = basic_font.render('Пауза: пробел', True, INFO_COLOR)
    pause_rect = pause_surf.get_rect()
    pause_rect.topleft = (WINDOW_WIDTH - 550, 420)
    display_surface.blit(pause_surf, pause_rect)

    esc_surf = basic_font.render('Выход: Esc', True, INFO_COLOR)
    esc_rect = esc_surf.get_rect()
    esc_rect.topleft = (WINDOW_WIDTH - 550, 450)
    display_surface.blit(esc_surf, esc_rect)


def draw_figure(fig, pixel_x=None, pixel_y=None):
    fig_to_draw = FIGURES[fig['shape']][fig['rotation']]

    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convert_coords(fig['x'], fig['y'])

    #отрисовка элементов фигур
    for x in range(FIG_WIDTH):
        for y in range(FIG_HEIGHT):
            if fig_to_draw[y][x] != EMPTY:
                draw_block(None, None, fig['color'],
                           pixel_x + (x * BLOCK_SIZE),
                           pixel_y + (y * BLOCK_SIZE))


def draw_next_figure(fig):  # превью следующей фигуры
    next_surf = basic_font.render('Следующая:', True, TXT_COLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 150, 180)
    display_surface.blit(next_surf, next_rect)

    draw_figure(fig, pixel_x=WINDOW_WIDTH-150, pixel_y=230)


if __name__ == '__main__':
    main()
