import pygame
import random
import csv

def block_mod_set(): 
    global block_blank_size, block_fill

    if block_mode == 1:
        block_blank_size = 1
        block_fill = 0

    elif block_mode == 2:
        block_blank_size = 1
        block_fill = 2

    elif block_mode == 3:
        block_blank_size = int(block_size * 1 / 2)
        block_fill = 0

    elif block_mode == 4:
        block_blank_size = 0
        block_fill = int(block_size * 1 / 3)

def draw_screen():
    global rows, columns, grid

    screen.fill((0, 0, 0))

    for row in range(rows):
        for col in range(columns):
            draw_game(grid[row][col], (row, col))

    draw_next()
    draw_score()
    draw_timer()
    draw_block_mode()
    draw_combo_text()
    draw_block()

def draw_game(color_idx, pos):
    global block_size, block_blank_size, block_fill

    x_pos = pos[0] * block_size + block_size * 2
    y_pos = pos[1] * block_size + block_size * 2

    block = pygame.Rect(0, 0, block_size - block_blank_size, block_size - block_blank_size)
    block.center = (y_pos, x_pos)

    pygame.draw.rect(screen, color[color_idx], block, block_fill)

def draw_next():
    global block_size, blocks_data, next_block, block_fill

    x_size = block_size * 5
    y_size = block_size * 10
    pygame.draw.rect(screen, (255, 255, 255), (21 * block_size, 22 * block_size - y_size, x_size, y_size), 2)

    size = block_size / 4 * 3

    for y in range(6):
        num = int(y / 2)
        k = y % 2
        idx = next_block[num]

        x_start = 23.5 * block_size - (len(blocks_data[idx - 1][0][0]) / 2) * size
        y_start = 12 * block_size + (num + 1) * block_size + (num + 0.5) * size

        if idx == 1 and k == 1:
            k = 0
        elif idx == 1 and k == 0:
            y += 1

        for x in range(len(blocks_data[idx - 1][0][k])):
            if blocks_data[idx - 1][0][k][x] == 1:
                block = pygame.Rect(x_start + x * size, y_start + y * size, size - block_blank_size * 3 / 4, size - block_blank_size * 3 / 4)
                pygame.draw.rect(screen, color[idx], block, block_fill)

    text = small_font.render("Next Blocks", True, color[next_block[0]])
    screen.blit(text, (21.15 * block_size, 11 * block_size))

def draw_timer():
    global remaining_time, timer_font, block_size, color

    x_size = block_size * 5
    y_size = block_size * 4
    pygame.draw.rect(screen, (255, 255, 255), (15 * block_size, 12 * block_size, x_size, y_size), 2)  # Timer box

    label_font = pygame.font.Font(None, int(block_size * 1.5))
    label_text = label_font.render("Time Remain", True, (255, 255, 255))
    screen.blit(label_text, (14.3 * block_size, 11 * block_size))  

    timer_text = timer_font.render(str(remaining_time).zfill(2), True, (255, 0, 0))  # Timer in red
    timer_text_rect = timer_text.get_rect(center=(17.5 * block_size, 14 * block_size))
    screen.blit(timer_text, timer_text_rect)


def draw_score():
    global score, score_title_font, score_font, block_size, color_idx, color

    x_size = block_size * 11
    y_size = block_size * 5
    pygame.draw.rect(screen, (255, 255, 255), (15 * block_size, 5 * block_size, x_size, y_size), 2)

    if color_idx >= 7:
        color_idx = 1
    else:
        color_idx += 0.001

    text = score_title_font.render("SCORE", True, color[curr_block_idx])
    screen.blit(text, (16.6 * block_size, 2.7 * block_size))

    score_text = score_font.render(str(score).zfill(7), True, color[int(color_idx)])
    score_text_rect = score_text.get_rect(center=(20.5 * block_size, 7.8 * block_size))
    screen.blit(score_text, score_text_rect)

def draw_block_mode():
    global mode_1, mode_2, mode_3, mode_4, block_mode

    button_size = int(block_size * 3 / 2)

    x_size = block_size * 5
    y_size = block_size * 4.5
    pygame.draw.rect(screen, (255, 255, 255), (15 * block_size, 17.5 * block_size, x_size, y_size), 2)

    text = small_font.render("Block Mode", True, (255, 255, 255))
    screen.blit(text, (15.15 * block_size, 16.4 * block_size))

    mode_1 = pygame.Rect(block_size * 15.1 + button_size * 0.4, block_size * 17.1 + button_size * 0.6, button_size, button_size)
    mode_2 = pygame.Rect(block_size * 17.9, block_size * 17.1 + button_size * 0.6, button_size, button_size)
    mode_3 = pygame.Rect(block_size * 15.1 + button_size * 0.4, block_size * 20, button_size, button_size)
    mode_4 = pygame.Rect(block_size * 17.9, block_size * 20, button_size, button_size)

    pygame.draw.rect(screen, (0, 0, 0), mode_1)
    pygame.draw.rect(screen, (0, 0, 0), mode_2)
    pygame.draw.rect(screen, (0, 0, 0), mode_3)
    pygame.draw.rect(screen, (0, 0, 0), mode_4)

    mode_1_color = [100, 100, 100]
    mode_2_color = [100, 100, 100]
    mode_3_color = [100, 100, 100]
    mode_4_color = [100, 100, 100]

    if block_mode == 1:
        mode_1_color = color[8]
    elif block_mode == 2:
        mode_2_color = color[8]
    elif block_mode == 3:
        mode_3_color = color[8]
    elif block_mode == 4:
        mode_4_color = color[8]

    block = pygame.Rect(block_size * 15.1 + 1 + button_size * 0.4, block_size * 17.1 + 1 + button_size * 0.6, button_size - 2, button_size - 2)
    pygame.draw.rect(screen, mode_1_color, block, 0)

    block = pygame.Rect(block_size * 17.9 + 1, block_size * 17.1 + 1 + button_size * 0.6, button_size - 2, button_size - 2)
    pygame.draw.rect(screen, mode_2_color, block, 4)

    block = pygame.Rect(block_size * 15.1 + int(button_size * 1 / 2) / 2 + button_size * 0.4, block_size * 20 + int(button_size * 1 / 2) / 2, button_size - int(button_size * 1 / 2), button_size - int(button_size * 1 / 2))
    pygame.draw.rect(screen, mode_3_color, block, 0)

    block = pygame.Rect(block_size * 17.9, block_size * 20, button_size, button_size)
    pygame.draw.rect(screen, mode_4_color, block, int(button_size * 1 / 3))

def block_pos_produce():
    global curr_block_idx, next_block, block_count, fall_turn, max_fall_turn, curr_block_idx, blocks_data, block_x_pos, block_y_pos, produce_ticks, curr_block_x_size, curr_block_y_size, curr_block_shape_idx, last_block_shape_idx, last_block_x_pos, last_block_y_pos

    # Select the current block from the next_block queue
    curr_block_idx = next_block[0]

    for i in range(len(next_block) - 1):
        next_block[i] = next_block[i + 1]
    next_block[2] = random.randint(1, 7)

    fall_turn = max((0.5 - 1.2) / 100 * block_count + 1.2, (max_fall_turn - 0.5) / (300 - 100) * (block_count - 100) + 0.5, max_fall_turn)

    curr_block_shape_idx = 0
    last_block_shape_idx = 0

    block_data = blocks_data[curr_block_idx - 1]
    curr_block = block_data[curr_block_shape_idx]
    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    block_x_pos = 5 + int(2.5 - curr_block_x_size)
    block_y_pos = 0

    last_block_x_pos = -1
    last_block_y_pos = -1

    produce_ticks = pygame.time.get_ticks()

def block_falling():
    global produce_ticks, now_ticks, fall_turn, block_y_pos, can_under, straight

    now_ticks = pygame.time.get_ticks()

    if straight:
        falling_finish()
        straight = False

    if (now_ticks - produce_ticks) / 1000 > fall_turn:
        produce_ticks = now_ticks
        now_ticks = pygame.time.get_ticks()
        if can_under:
            block_y_pos += 1
            can_under = False
        else:
            falling_finish()

def falling_finish():
    global curr_block_idx, block_y_pos, running, block_count
    #, block_score, score

    block_clear_check()

    block_count += 1

    if block_y_pos <= 0:
        cause_motion()
        running = False
    else:
        block_pos_produce()

    #score += block_score

def draw_block():
    global curr_block_idx, curr_block_shape_idx, block_x_pos, block_y_pos, last_block_x_pos, last_block_y_pos, last_block_shape_idx, curr_block_x_size, curr_block_y_size, last_block_x_size, last_block_y_size

    block_data = blocks_data[curr_block_idx - 1]

    curr_block = block_data[curr_block_shape_idx]
    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    last_block = block_data[last_block_shape_idx]
    last_block_size_x = len(last_block[0])
    last_block_size_y = len(last_block)

    if last_block_x_pos > -1:
        for x in range(last_block_size_x):
            for y in range(last_block_size_y):
                if last_block[y][x] == 1:
                    grid[y + last_block_y_pos][x + last_block_x_pos] = 0

    for x in range(curr_block_x_size):
        for y in range(curr_block_y_size):
            if curr_block[y][x] == 1:
                grid[y + block_y_pos][x + block_x_pos] = curr_block_idx

    last_block_x_pos = block_x_pos
    last_block_y_pos = block_y_pos
    last_block_shape_idx = curr_block_shape_idx

def block_right():
    global block_x_pos, can_right

    if can_right:
        block_x_pos += 1

def block_left():
    global block_x_pos, can_left

    if can_left:
        block_x_pos -= 1

def block_up():
    global block_y_pos

    block_y_pos -= 1

def block_rotate():
    global curr_block_shape_idx, blocks_data, block_x_pos, curr_block_x_size, curr_block_y_size, block_y_pos, can_under_size, can_up_size, can_right_size, can_left_size, can_rotate

    block_data = blocks_data[curr_block_idx - 1]

    can_horizontal_size = min(can_right_size) + min(can_left_size) + curr_block_x_size
    can_vertical_size = min(can_under_size) + min(can_up_size) + curr_block_y_size

    can_rotate = True

    if can_horizontal_size >= curr_block_y_size:  # rotate
        if (min(can_up_size) == 100) and (min(can_under_size) + curr_block_y_size + block_y_pos > curr_block_x_size): # rotate
            can_rotate = True
        else:
            if can_vertical_size >= curr_block_x_size and (min(can_under_size) + curr_block_y_size + block_y_pos > curr_block_x_size):  # rotate
                can_rotate = True
            else:
                can_rotate = False
    else:  # can't rotate
        can_rotate = False

    if can_rotate:
        if min(can_right_size) < curr_block_y_size:
            for i in range(curr_block_y_size - (curr_block_x_size + min(can_right_size))):
                block_left()

        if min(can_under_size) < curr_block_x_size:
            for i in range(curr_block_x_size - (curr_block_y_size + min(can_under_size))):
                block_up()

        if (curr_block_idx == 4) and (curr_block_shape_idx == 0):
            if can_under_size[0] == 0:
                if can_up_size[1] == 1:
                    curr_block_shape_idx -= 1
                else:
                    block_up()

        if (curr_block_idx == 5) and (curr_block_shape_idx == 2):
            if can_under_size[1] == 0:
                block_up()

        if (curr_block_idx == 6) and (curr_block_shape_idx == 2):
            if (can_under_size[0] == 0) or (can_under_size[1] == 0):
                block_up()

        if (curr_block_idx == 6) and (curr_block_shape_idx == 1):
            if can_under_size[1] == 0:
                block_up()

        if curr_block_shape_idx < len(block_data) - 1:
            curr_block_shape_idx += 1
        else:
            curr_block_shape_idx = 0

def block_down():
    global block_y_pos, can_under

    if can_under:
        block_y_pos += 1
        can_under = False

def block_can_right_check():
    global block_x_pos, block_y_pos, can_right, blocks_data, curr_block_idx, curr_block_shape_idx, curr_block_x_size, curr_block_y_size, grid, can_right_size

    can_right = False
    can_right_size = []

    block_data = blocks_data[curr_block_idx - 1]
    curr_block = block_data[curr_block_shape_idx]
    block_margin_x = curr_block_x_size - 1

    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    for y in range(curr_block_y_size):
        for x in range(curr_block_x_size - 1, -1, -1):
            if curr_block[y][x] == 1:
                block_margin_x = x
                break

        for x in range(block_x_pos + block_margin_x + 1, 12, 1):
            if grid[y + block_y_pos][x] > 0:
                can_right_size.append(x - (block_x_pos + block_margin_x) - 1)
                break

    if min(can_right_size) == 0:
        can_right = False
    else:
        can_right = True

def block_can_left_check():
    global block_x_pos, block_y_pos, can_left, blocks_data, curr_block_idx, curr_block_shape_idx, curr_block_x_size, curr_block_y_size, grid, can_left_size

    can_left = False
    can_left_size = []

    block_data = blocks_data[curr_block_idx - 1]
    curr_block = block_data[curr_block_shape_idx]
    block_margin_x = 0

    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    for y in range(curr_block_y_size):
        for x in range(curr_block_x_size):
            if curr_block[y][x] == 1:
                block_margin_x = x
                break

        for x in range(block_x_pos + block_margin_x - 1, -1, -1):
            if grid[y + block_y_pos][x] > 0:
                can_left_size.append((block_x_pos + block_margin_x) - x - 1)
                break

    if min(can_left_size) == 0:
        can_left = False
    else:
        can_left = True

def block_can_under_check(): #한 칸 아래로 내려갈 수 있는지 확인
    global block_x_pos, block_y_pos, can_under, blocks_data, curr_block_idx, curr_block_shape_idx, curr_block_x_size, curr_block_y_size, grid, can_under_size

    can_under = False
    can_under_size = []

    block_data = blocks_data[curr_block_idx - 1]
    curr_block = block_data[curr_block_shape_idx]
    block_bottom_y = curr_block_y_size - 1

    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    for x in range(curr_block_x_size):
        for y in range(curr_block_y_size - 1, -1, -1):
            if curr_block[y][x] == 1:
                block_bottom_y = y
                break

        for y in range(block_y_pos + block_bottom_y + 1, 21, 1):
            if grid[y][x + block_x_pos] > 0:
                can_under_size.append(y - (block_y_pos + block_bottom_y) - 1)
                break

    if min(can_under_size) == 0:
        can_under = False
    else:
        can_under = True

def block_can_up_check():
    global block_x_pos, block_y_pos, blocks_data, curr_block_idx, curr_block_shape_idx, curr_block_x_size, curr_block_y_size, grid, can_up_size

    can_up_size = []

    block_data = blocks_data[curr_block_idx - 1]
    curr_block = block_data[curr_block_shape_idx]
    block_top_y = 0

    curr_block_x_size = len(curr_block[0])
    curr_block_y_size = len(curr_block)

    for x in range(curr_block_x_size):
        for y in range(curr_block_y_size):
            if curr_block[y][x] == 1:
                block_top_y = y
                break

        for y in range(block_y_pos + block_top_y - 1, -1, -1):
            if grid[y][x + block_x_pos] > 0:
                can_up_size.append((block_y_pos + block_top_y) - y - 1)
                break

            if y == 0:
                can_up_size.append(100)

        if block_y_pos + block_top_y == 0:
            can_up_size.append(100)

def block_straight():
    global can_under_size, block_y_pos, straight, straight_score, score

    block_y_pos += min(can_under_size)
    straight = True

    #score += straight_score * min(can_under_size)

def block_clear_check():
    global grid, columns, rows, clear_score, score, clear_combo, draw_combo, clear_row_y_pos

    now_clear_rows = 0

    for row in range(0, rows - 1, 1):
        check = 1
        for col in range(columns):
            check *= grid[row][col]

        if check > 0:
            clear(row)
            clear_row_y_pos = row * block_size + block_size * 2
            now_clear_rows += 1

    if not now_clear_rows == 0:
        clear_combo += 1
        draw_combo = 1
    else:
        clear_combo = 0
        draw_combo = 0

    score += clear_score * ((now_clear_rows) ** 2) * int(clear_combo ** (3 / 2))

def draw_combo_text():
    global combo_ticks, now_ticks, draw_combo

    now_ticks = pygame.time.get_ticks()

    if clear_combo >= 2:
        if draw_combo == 1:
            if combo_ticks == None:
                combo_ticks = pygame.time.get_ticks()

            elif now_ticks - combo_ticks <= 1000:
                combo_text = combo_font.render("Combo X " + str(clear_combo), True, (255, 255, 255))
                combo_text_rect = combo_text.get_rect(center=(20.5 * block_size, 6.1 * block_size))

                screen.blit(combo_text, combo_text_rect)

            else:
                combo_ticks = None
                draw_combo = 0

def clear(clear_row):
    global grid, columns, rows

    list1 = [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]
    list2 = [i for i in grid[clear_row]]

    for i in range(6):
        if i % 2 == 0:
            grid[clear_row] = list1
        else:
            grid[clear_row] = list2

        for row in range(rows):
            for col in range(columns):
                draw_game(grid[row][col], (row, col))
        pygame.display.update()

        pygame.time.delay(100)

    for row in range(clear_row, 0, -1):
        grid[row] = grid[row - 1]

    grid[0] = [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]

def cause_motion():
    global grid

    list1 = [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]
    list2 = [i for i in grid[0]]

    for i in range(8):
        if i % 2 == 0:
            grid[0] = list1
        else:
            grid[0] = list2

        for row in range(rows):
            for col in range(columns):
                draw_game(grid[row][col], (row, col))
        pygame.display.update()

        pygame.time.delay(100)

def game_over():
    for y in range(21):
        for x in range(12):
            x_pos = x * block_size + block_size * 2
            y_pos = y * block_size + block_size * 2

            block = pygame.Rect(0, 0, block_size - block_blank_size, block_size - block_blank_size)
            block.center = (x_pos, y_pos)

            pygame.draw.rect(screen, color[8], block, block_fill)

        pygame.display.update()

        pygame.time.delay(100)

def check_buttons(pos):
    global mode_1, mode_2, mode_3, mode_4, block_mode

    if mode_1.collidepoint(pos):
        block_mode = 1
    elif mode_2.collidepoint(pos):
        block_mode = 2
    elif mode_3.collidepoint(pos):
        block_mode = 3
    elif mode_4.collidepoint(pos):
        block_mode = 4

pygame.init()

block_size = 24


remaining_time = 180  # Set the timer to 120 seconds
key_presses = [] # list of butons pressed by the user in chronological order
timer_font = pygame.font.Font(None, int(block_size * 3))  # Font for timer text
last_timer_tick = pygame.time.get_ticks()  # Tracks time for decrement


screen_width = block_size * 28 # 가로
screen_height = block_size * 24  # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("3MIN TETRIS")
##############################################################

background_1 = [(0, i) for i in range(21)]
background_2 = [(i, 20) for i in range(12)]
background_3 = [(11, i) for i in range(21)]
background = background_1 + background_2 + background_3

columns = 12
rows = 21

grid = [[0 for col in range(columns)] for row in range(rows)]
miri_grid = [[0 for col in range(columns)] for row in range(rows)]

for pos in background:
    grid[pos[1]][pos[0]] = 8

block_mode = 1

block_blank_size = 1
block_fill = 0

block_count = 1

score = 0

#straight_score = 3
falling_score = 1
#block_score = 15
clear_score = 100

clear_combo = 0
draw_combo = 0
clear_row_y_pos = 0

draw_increase_score = 0

small_font = pygame.font.Font(None, int(block_size * 5 / 4))
score_font = pygame.font.Font(None, int(block_size * 3.5))
score_title_font = pygame.font.Font(None, int(block_size * 2.5))
combo_font = pygame.font.Font(None, int(block_size))

color_idx = 1

block_x_pos = 0
block_y_pos = 0
curr_block_shape_idx = 0
curr_block_x_size = 0
curr_block_y_size = 0

last_block_x_pos = -1
last_block_y_pos = -1
last_block_shape_idx = 0
last_block_x_size = 0
last_block_y_size = 0

next_block = [random.randint(1, 7), random.randint(1, 7), random.randint(1, 7)]
curr_block_idx = 0

# black, light-blue, yellow, green, red, orange, blue, purple, grey
color = [(0, 0, 0), (0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 127, 0), (0, 0, 255), (168, 64, 255), (195, 195, 195)]

blocks_data = [
    [
    [[1, 1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]]
    ], #하늘색 1

    [
    [[1, 1],
     [1, 1]]
    ], #노란색 2

    [
    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 0],
     [1, 1],
     [0, 1]]
    ], #초록색 3

    [
    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1],
     [1, 1],
     [1, 0]]
    ], #빨간색 4

    [
    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1],
     [0, 1],
     [0, 1]]
    ], #주황색 5

    [
    [[1, 0, 0],
     [1, 1, 1]],

    [[1, 1],
     [1, 0],
     [1, 0]],

    [[1, 1, 1],
     [0, 0, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]]
    ], #파란색 6

    [
    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 0],
     [1, 1],
     [1, 0]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1],
     [1, 1],
     [0, 1]]
    ],  # 보라색 7
]

combo_ticks = None
produce_ticks = None
now_ticks = None
fall_turn = 1
max_fall_turn = 0.15

can_under_size = []
can_under = True
can_right_size = []
can_right = True
can_left_size = []
can_left = True
can_up_size = []

can_rotate = True
straight = False

mode_1 = pygame.Rect(0, 0, 0, 0)
mode_2 = pygame.Rect(0, 0, 0, 0)
mode_3 = pygame.Rect(0, 0, 0, 0)
mode_4 = pygame.Rect(0, 0, 0, 0)

click_pos = None

block_pos_produce()

running = True
while running:
    block_mod_set()

    block_can_up_check()
    block_can_under_check()
    block_can_right_check()
    block_can_left_check()

    block_falling()

    # Update the timer
    current_ticks = pygame.time.get_ticks()
    if current_ticks - last_timer_tick >= 1000:  # Decrease every second
        remaining_time -= 1
        last_timer_tick = current_ticks

    # Stop the game if the timer runs out
    if remaining_time <= 0:
        running = False  # End the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_presses.append(pygame.key.name(event.key))  # Record the name of the key pressed
            #Handle key presses for game controls
            if event.key == pygame.K_RIGHT:
                block_right()
            elif event.key == pygame.K_LEFT:
                block_left()
            elif event.key == pygame.K_UP:
                block_rotate()
            elif event.key == pygame.K_DOWN:
                block_down()
                #score += falling_score
            elif event.key == pygame.K_SPACE:
                block_straight()
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            check_buttons(click_pos)

    draw_screen()
    pygame.display.update()

pygame.time.delay(500)

game_over()
pygame.quit()

# Save key presses and final score to CSV
csv_filename = "game_record.csv"

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([", ".join(key_presses), score])  # Record key presses and final score

print(f"Game record saved to {csv_filename}")