import pygame
import random

TILE_SIZE = 20
FREE_TILES = [1, 5]
FREE_TILES_FOR_ENEMY = [1, 2, 5]
ENEMY_EVENT = 20


def main():
    pygame.init()
    size = 560, 660
    screen = pygame.display.set_mode(size)
    # счет игрока на начало игры
    score = 0
    # создание экзепляра лабиринта (из текствого файла в матрицу)
    labyrinth = Labyrinth()
    # создание экземпляра пакмана
    pacman = Pacman(labyrinth)
    # создание экземпляра точек
    dots = Dots()
    # создание экземпляра точки-бонуса
    bonus = Bonus(score)
    # создание экземпляра приведения
    red_enemy = Enemy((252, 44, 0), 1)
    pink_enemy = Enemy((253, 192, 179), 2)
    # создание экземпляра PacmanMoves, который задает движение пакмана
    pacman_moves = PacmanMoves(screen, labyrinth, pacman, score, dots, red_enemy, pink_enemy, bonus)
    clock = pygame.time.Clock()
    game_over = False
    running = True
    while running and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENEMY_EVENT:
                pacman_moves.move_enemy()
                pacman_moves.move_pink_enemy()
        # перемещение пакмана
        pacman_moves.change_pos(screen)
        screen.fill((0, 0, 0))
        # создание изображений элементов игры
        pacman_moves.make()
        if pacman_moves.won() or pacman_moves.lost():
            game_over = True
        pygame.display.flip()
        clock.tick(15)
    pygame.quit()


class Labyrinth:
    def __init__(self):
        self.map = []
        with open("pacman_light_labyrinth.txt") as text_lab:
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
        if distance[y][x] == lasted or first_pos == second_pos:
            return first_pos
        while past[y][x] != first_pos:
            x, y = past[y][x]
        return x, y


class Pacman:
    def __init__(self, labyrinth):
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
        x = random.randint(0, 27)
        y = random.randint(0, 27)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(0, 27)
            y = random.randint(0, 27)
        return x, y


class Enemy:
    def __init__(self, color, number):
        self.number = number
        self.x, self.y = self.start_position()
        self.delay = 200
        pygame.time.set_timer(ENEMY_EVENT, self.delay)
        self.color = color

    def start_position(self):
        if self.number == 1:
            return 11, 14
        elif self.number == 2:
            return 16, 14
        
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def make(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, 25 + self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color, center, TILE_SIZE // 2)


class PacmanMoves:
    def __init__(self, screen, labyrinth, pacman, score, dots, red_enemy, pink_enemy, bonus):
        self.enemy1 = red_enemy
        self.enemy2 = pink_enemy
        self.screen = screen
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.score = score
        self.dots = dots
        self.bonus = bonus

    def make(self):
        self.labyrinth.make(self.screen)
        self.pacman.make(self.screen)
        self.dots.make_dots(self.screen, self.labyrinth)
        self.enemy1.make(self.screen)
        self.enemy2.make(self.screen)
        self.bonus.make(self.screen, self.labyrinth)

    # изменение позиции пакмана
    def change_pos(self, screen):
        new_x, new_y = self.pacman.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT] and new_x == 0:
            new_x += 27
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x -= 1
            # если эта точка имеет "точку", выполняется функция "plus_point"
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        if pygame.key.get_pressed()[pygame.K_RIGHT] and new_x == 27:
            new_x -= 27
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x += 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_y -= 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
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

    def move_enemy(self):
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

    def won(self):
        if self.labyrinth.maximum_score == 0:
            return True

    def lost(self):
        return self.pacman.get_position() == self.enemy1.get_position()


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
    main()
