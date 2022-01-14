import pygame
import random

TILE_SIZE = 20
FREE_TILES = [1, 5]
ENEMY_EVENT_TYPE = 30


def main():
    pygame.init()
    size = 560, 600
    screen = pygame.display.set_mode(size)
    # счет игрока на начало игры
    score = 0
    # создание экзепляра лабиринта (из текствого файла в матрицу)
    labyrinth = Labyrinth()
    # создание экземпляра пакмана
    pacman = Pacman(labyrinth)
    enemy = Enemy((1, 1))
    # создание экземпляра точек
    dots = Dots()
    enemy = Enemy((1, 1))
    # создание экземпляра PacmanMoves, который задает движение пакмана
    pacman_moves = PacmanMoves(screen, labyrinth, pacman, score, dots, enemy)
    # создание экземпляра точки-бонуса
    bonus = Bonus(score)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENEMY_EVENT_TYPE:
                pacman_moves.move_enemy()
        # перемещение пакмана
        pacman_moves.change_pos(screen)
        screen.fill((0, 0, 0))
        # создание самого лабиринта (из матрицы в виджет pygame)
        pacman_moves.make()
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
        # цвета для  каждого символа в лабиринте
        # 0 - стена,
        # 1 - можно ходить(по белому), де есть точки,
        # 5 - можно ходить, но точек нет,
        # 9 - место за полем,
        # 2 - могут ходить только приведения
        colors = {0: (0, 0, 120), 1: (255, 255, 255),
                  9: (0, 0, 0), 2: (0, 100, 0), 5: (255, 255, 255)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def tile_is_free(self, position):
        return self.get_tile_id(position) in FREE_TILES

    def find_path_step(self, start, target):
        lasted = 1000
        x, y = start
        distance = [[lasted] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        past = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                        self.tile_is_free((next_x, next_y)) and distance[next_y][next_x] == lasted:
                    distance[next_y][next_x] = distance[y][x] + 1
                    past[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == lasted or start == target:
            return start
        while past[y][x] != start:
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
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 2)

    def start_position(self, labyrinth):
        x = random.randint(0, 27)
        y = random.randint(0, 27)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(0, 27)
            y = random.randint(0, 27)
        return x, y


class Enemy:
    def __init__(self, position):
        self.x, self.y = position
        self.delay = 200
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        
    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def make(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 120, 120), center, TILE_SIZE // 2)


class PacmanMoves:
    def __init__(self, screen, labyrinth, pacman, score, dots, enemy):
        self.screen = screen
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.score = score
        self.dots = dots
        self.enemy = enemy

    def make(self):
        self.labyrinth.make(self.screen)
        self.pacman.make(self.screen)
        self.dots.make_dots(self.screen, self.labyrinth)
        self.enemy.make(self.screen)

    def change_pos(self, screen):
        # зменение позиции пакмана
        new_x, new_y = self.pacman.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT] and new_x == 0:
            new_x += 27
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x -= 1
            # если эта точка имеет "точку", выполняется функция "plus_point"
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
        if pygame.key.get_pressed()[pygame.K_RIGHT] and new_x == 27:
            new_x -= 27
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x += 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_y -= 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            new_y += 1
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
        # проверка : свободна ли клетка
        if self.labyrinth.tile_is_free((new_x, new_y)):
            self.pacman.set_position((new_x, new_y))

    # прибавляется 10 очков к "score" и стирается точка
    def plus_point(self, screen, new_x, new_y):
        self.labyrinth.map[new_y][new_x] = 5
        self.score += 10
        center = new_x * TILE_SIZE + TILE_SIZE // 2, new_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 0, 0), center, TILE_SIZE // 2)

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(),
                                                      self.pacman.get_position())
        self.enemy.set_position(next_position)


class Dots:
    def __init__(self):
        pass

    def make_dots(self, screen, labyrinth):
        for i in range(len(labyrinth.map)):
            for j in range(len(labyrinth.map[0])):
                if labyrinth.map[i][j] == 1:
                    center = j * TILE_SIZE + TILE_SIZE // 2, \
                             i * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 5)


class Bonus:
    def __init__(self, score):
        self.score = score


if __name__ == '__main__':
    main()
