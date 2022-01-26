import pygame

TILE_SIZE = 20
FREE_TILES = [1, 5]
FREE_TILES_FOR_ENEMY = [1, 2, 5]
YELLOW = (245, 208, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 80)
GREY = (130, 130, 120)
BLUE_FOR_BORDERS = (0, 0, 120)


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
        # цвета для  каждого символа в лабиринте:
        # 0 - стена,
        # 1 - можно ходить(по белому), де есть точки,
        # 2 - могут ходить только приведения,
        # 3 - места для бонусов,
        # 5 - можно ходить, но точек нет,
        # 9 - место за полем
        colors = {0: BLUE_FOR_BORDERS, 1: WHITE, 3: WHITE,
                  9: BLACK, 2: WHITE, 5: WHITE}
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
        distance = []
        for _ in range(self.height):
            distance.append([lasted] * self.width)
        distance[y][x] = 0
        past = []
        for _ in range(self.height):
            past.append([None] * self.width)
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