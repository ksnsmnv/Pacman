import pygame
import random

WIDTH, HEIGHT = 560, 650
TILE_SIZE = 20
FREE_TILES = [1, 5]
FREE_TILES_FOR_ENEMY = [1, 2, 5]
ENEMY_EVENT = 20
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
YELLOW = (245, 208, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 80)
pygame.font.init()


# оздание текстового объекта
def text_objects(text, font, color=WHITE):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# создание конпки с функционалом
def button(msg, x, y, w, h, ic, ac, action=''):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
        if click[0] == 1 and action:
            if action == 'level1_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 350, (15, 30))
            if action == 'level2_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 250, (10, 25))
            if action == 'level3_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 200, (5, 20))
            if action == 'level1_2':
                main((560, 650), 'pacman_labyrinth.txt', 350, (30, 45))
            if action == 'level2_2':
                main((560, 650), 'pacman_labyrinth.txt', 250, (20, 35))
            if action == 'level3_2':
                main((560, 650), 'pacman_labyrinth.txt', 200, (15, 30))
            elif action == 'quit':
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(DISPLAY, ic, (x, y, w, h))

    small_text = pygame.font.Font(None, 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), y + (h / 2))
    DISPLAY.blit(text_surf, text_rect)


# создание экрана меню
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        DISPLAY.fill(DARK_BLUE)
        large_text = pygame.font.Font(None, 115)
        text_surf, text_rect = text_objects("PAC-MAN", large_text, YELLOW)
        text_rect.center = ((WIDTH / 2), (HEIGHT / 4))
        DISPLAY.blit(text_surf, text_rect)

        button("Labyrinth 1:", WIDTH / 6, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6, 300, 100, 50, DARK_BLUE, BLACK, 'level1_1')
        button("Level 2", WIDTH / 6, 375, 100, 50, DARK_BLUE, BLACK, 'level2_1')
        button("Level 3", WIDTH / 6, 450, 100, 50, DARK_BLUE, BLACK, 'level3_1')

        button("Labyrinth 2:", WIDTH / 6 * 3.7, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6 * 3.7, 300, 100, 50, DARK_BLUE, BLACK, 'level1_2')
        button("Level 2", WIDTH / 6 * 3.7, 375, 100, 50, DARK_BLUE, BLACK, 'level2_2')
        button("Level 3", WIDTH / 6 * 3.7, 450, 100, 50, DARK_BLUE, BLACK, 'level3_2')

        button("Quit", 220, 520, 100, 50, DARK_BLUE, BLACK, 'quit')
        pygame.display.update()
        pygame.time.Clock().tick(15)


def main(size, file_name, speed, start):
    pygame.init()
    screen = pygame.display.set_mode(size)
    # счет игрока на начало игры
    score = 0
    # создание экзепляра лабиринта (из текствого файла в матрицу)
    labyrinth = Labyrinth(file_name)
    # создание экземпляра пакмана
    pacman = Pacman(labyrinth)
    # создание экземпляра точек
    dots = Dots()
    # создание экземпляра точки-бонуса
    bonus = Bonus(score)
    # создание экземпляров приведений
    red_enemy = Enemy((252, 44, 0), 1, speed)
    pink_enemy = Enemy((253, 192, 179), 2, speed)
    orange_enemy = Enemy((255, 140, 0), 3, speed)
    # создание экземпляра PacmanMoves, который задает движение пакмана и приведений
    pacman_moves = PacmanMoves(screen, labyrinth, pacman, score, dots, red_enemy, pink_enemy, orange_enemy, bonus)

    clock = pygame.time.Clock()
    game_over = False
    running = True

    while running and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_intro()
            elif event.type == ENEMY_EVENT:
                if pacman_moves.flag2(start):
                    pacman_moves.move_red_enemy()
                if pacman_moves.flag(start):
                    pacman_moves.move_pink_enemy()
                pacman_moves.move_orange_enemy()
        # перемещение пакмана
        pacman_moves.change_pos(screen)
        screen.fill((0, 0, 0))
        # создание изображений элементов игры
        pacman_moves.make()
        # проверка на то, выиграл или проиграл ли игрок
        if pacman_moves.won() or pacman_moves.lost(1) or pacman_moves.lost(2) or pacman_moves.lost(3):
            game_over = True
            game_intro()
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()


class Labyrinth:
    def __init__(self, file_name):
        self.map = []
        with open(file_name) as text_lab:
            for line in text_lab:
                # создание матрицы либиринта
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])

    def make(self, screen):
        self.maximum_score = 0
        # цвета для  каждого символа в лабиринте
        # 0 - стена,
        # 1 - можно ходить(по белому), де есть точки,
        # 5 - можно ходить, но точек нет,
        # 3 - места для бонусов,
        # 9 - место за полем,
        # 2 - могут ходить только приведения
        colors = {0: (0, 0, 120), 1: (255, 255, 255), 3: (255, 255, 255),
                  9: (0, 0, 0), 2: (130, 130, 120), 5: (255, 255, 255)}
        for y in range(self.height):
            for x in range(self.width):
                if self.get_tile_id((x, y)) == 1:
                    self.maximum_score += 10
                elif self.get_tile_id((x, y)) == 3:
                    self.maximum_score += 50
                rect = pygame.Rect(x * TILE_SIZE, 25 + y * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    # свободна ли клетка для пакмна
    def tile_is_free(self, position):
        return self.get_tile_id(position) in FREE_TILES

    # свободна ли клетка для приведений
    def tile_is_free_for_enemy(self, position):
        return self.get_tile_id(position) in FREE_TILES_FOR_ENEMY

    # один шаг для приведения
    def find_path_step(self, first_pos, second_pos):
        lasted = 1000
        x, y = first_pos
        distance = [[lasted] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        past = [[None] * self.width for _ in range(self.height)]
        q = [(x, y)]
        while q:
            x, y = q.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.tile_is_free_for_enemy((next_x, next_y)) and distance[next_y][next_x] == lasted:
                    distance[next_y][next_x] = distance[y][x] + 1
                    past[next_y][next_x] = (x, y)
                    q.append((next_x, next_y))
        x, y = second_pos
        # проверка: был ли на этой клетке пакман или нет
        if distance[y][x] == lasted or first_pos == second_pos:
            return first_pos
        while past[y][x] != first_pos:
            x, y = past[y][x]
        return x, y


class Pacman:
    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        self.x, self.y = self.start_position(labyrinth)

    def set_position(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def make(self, screen):
        # создание пакмана в виде шарика
        center = self.x * TILE_SIZE + TILE_SIZE // 2, 25 + self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 2)

    def start_position(self, labyrinth):
        x = random.randint(0, self.labyrinth.width)
        y = random.randint(0, self.labyrinth.height)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(0, self.labyrinth.width)
            y = random.randint(0, self.labyrinth.height)
        return x, y


class Enemy:
    # создание врага, скорость которого задается в меню пакмана
    # чем выше уровень, тем выше скорость
    def __init__(self, color, number, speed):
        self.x, self.y = self.start_position(number)
        self.speed = speed
        pygame.time.set_timer(ENEMY_EVENT, self.speed)
        self.color = color

    # начальная позиция пакмана
    def start_position(self, number):
        if number == 1:
            return 1, 1
        elif number == 2:
            return 2, 1
        elif number == 3:
            return 3, 1
        
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def make(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, 25 + self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color, center, TILE_SIZE // 2)


class PacmanMoves:
    def __init__(self, screen, labyrinth, pacman, score, dots, red_enemy, pink_enemy, orange_enemy, bonus):
        # инициализация частей программы, которые требуются для выполнения функций этого класса
        self.enemy1 = red_enemy
        self.enemy2 = pink_enemy
        self.enemy3 = orange_enemy
        self.screen = screen
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.score = score
        self.dots = dots
        self.bonus = bonus
        self.points = 0

    # создание сех частей лабиринта в одной функции
    def make(self):
        self.labyrinth.make(self.screen)
        self.pacman.make(self.screen)
        self.dots.make_dots(self.screen, self.labyrinth)
        self.enemy1.make(self.screen)
        self.enemy2.make(self.screen)
        self.enemy3.make(self.screen)
        self.bonus.make(self.screen, self.labyrinth)

    # изменение позиции пакмана
    def change_pos(self, screen):
        new_x, new_y = self.pacman.get_position()
        # --- проверка нажатия клавиш ---
        # для левой клавиши
        if pygame.key.get_pressed()[pygame.K_LEFT] and new_x == 0:
            new_x += 27
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x -= 1
            # если эта точка имеет "точку", выполняется функция "plus_point"
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
                self.points += 1
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для правой клавиши
        if pygame.key.get_pressed()[pygame.K_RIGHT] and new_x == 27:
            new_x -= 27
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x += 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для верхней клавиши
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_y -= 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для нижней клавиши
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            new_y += 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # проверка : свободна ли клетка
        if self.labyrinth.tile_is_free((new_x, new_y)):
            self.pacman.set_position((new_x, new_y))

    # прибавляется 10 очков к "score" и стирается точка
    def plus_point(self, screen, new_x, new_y):
        self.labyrinth.map[new_y][new_x] = 5
        self.score += 10
        center = new_x * TILE_SIZE + TILE_SIZE // 2, 25 + new_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 0, 0), center, TILE_SIZE // 2)

    def plus_bonus(self, screen, new_x, new_y):
        self.labyrinth.map[new_y][new_x] = 5
        self.score += 50
        center = new_x * TILE_SIZE + TILE_SIZE // 2, 25 + new_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 0, 0), center, TILE_SIZE // 2)

    def move_red_enemy(self):
        # переход к функции find_path_step для получения следующей позиции
        next_position = self.labyrinth.find_path_step(self.enemy1.get_position(),
                                                      self.pacman.get_position())
        self.enemy1.set_position(next_position)

    def move_pink_enemy(self):
        position = self.pacman.get_position()
        if self.labyrinth.tile_is_free_for_enemy((position[0], position[1] - 4)):
            next_position = self.labyrinth.find_path_step(self.enemy2.get_position(),
                                                          (position[0], position[1] - 4))
            self.enemy2.set_position(next_position)
        elif self.labyrinth.tile_is_free_for_enemy((position[0] - 4, position[1])):
            next_position = self.labyrinth.find_path_step(self.enemy2.get_position(),
                                                          (position[0] - 4, position[1]))
            self.enemy2.set_position(next_position)

    def move_orange_enemy(self):
        position = self.pacman.get_position()
        position2 = self.enemy3.get_position()
        if abs(position2[0] - position[0]) <= 12 and abs(position2[1] - position[1]) <= 12:
            next_position = self.labyrinth.find_path_step(position2,
                                                          position)
            self.enemy3.set_position(next_position)
        else:
            step_x = random.randint(0, 27)
            step_y = random.randint(0, 28)
            while not self.labyrinth.tile_is_free_for_enemy((step_x, step_y)):
                step_x = random.randint(0, 27)
                step_y = random.randint(0, 28)
            next_position = self.labyrinth.find_path_step(position2,
                                                          (step_x, step_y))
            self.enemy3.set_position(next_position)

    # флаг для активации второго приведения
    def flag(self, start):
        if self.points >= start[0]:
            return True

    # флаг для активации первого приведения
    def flag2(self, start):
        if self.points >= start[1]:
            return True

    # проверка: закончились ли точки
    def won(self):
        if self.labyrinth.maximum_score == 0:
            return True

    # проверка: столкнулся ли пакман с приведением
    def lost(self, number_of_ghost):
        if number_of_ghost == 1:
            return self.pacman.get_position() == self.enemy1.get_position()
        if number_of_ghost == 2:
            return self.pacman.get_position() == self.enemy2.get_position()
        if number_of_ghost == 3:
            return self.pacman.get_position() == self.enemy3.get_position()


class Dots:
    def __init__(self):
        pass

    def make_dots(self, screen, labyrinth):
        for i in range(len(labyrinth.map)):
            for j in range(len(labyrinth.map[0])):
                if labyrinth.map[i][j] == 1:
                    center = j * TILE_SIZE + TILE_SIZE // 2, 25 + i * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 6)


class Bonus:
    def __init__(self, score):
        self.score = score

    def make(self, screen, labyrinth):
        self.all_bonus = 0
        for i in range(len(labyrinth.map)):
            for j in range(len(labyrinth.map[0])):
                if labyrinth.map[i][j] == 3:
                    center = j * TILE_SIZE + TILE_SIZE // 2, 25 + i * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 3)
                    self.all_bonus += 1

    def get_bonus(self):
        return self.all_bonus * 50


if __name__ == '__main__':
    game_intro()
