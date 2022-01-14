import pygame
import random


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
FPS = 15
TILE_SIZE = 20
ENEMY_EVENT_TYPE = 30
FREE_TILES = [1, 5]


class Labyrinth:
    def __init__(self, filename):
        self.map = []
        with open("maps/{}".format(filename)) as text_lab:
            for line in text_lab:
                # создание матрицы либиринта
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = FREE_TILES

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
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

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
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == lasted:
                    distance[next_y][next_x] = distance[y][x] + 1
                    past[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == lasted or start == target:
            return start
        while past[y][x] != start:
            x, y = past[y][x]
        return x, y


class Hero:
    def __init__(self, labyrinth):
        self.x, self.y = self.start_position(labyrinth)

    def start_position(self, labyrinth):
        x = random.randint(0, 27)
        y = random.randint(0, 27)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(0, 27)
            y = random.randint(0, 27)
        return x, y

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def make(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 0, 0), center, TILE_SIZE // 2)


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


class Moves:
    def __init__(self, labyrinth, hero, enemy):
        self.labyrinth = labyrinth
        self.hero = hero
        self.enemy = enemy

    def make(self, screen):
        self.labyrinth.make(screen)
        self.hero.make(screen)
        self.enemy.make(screen)

    def update_hero(self):
        nx, ny = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            nx -= 1
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            nx += 1
        elif pygame.key.get_pressed()[pygame.K_UP]:
            ny -= 1
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            ny += 1
        if self.labyrinth.is_free((nx, ny)):
            self.hero.set_position((nx, ny))

    def move_enemy(self):
        next_position = self.labyrinth.find_path_step(self.enemy.get_position(),
                                                      self.hero.get_position())
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


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labyrinth = Labyrinth('simple_map.txt')
    hero = Hero(labyrinth)
    enemy = Enemy((1, 1))
    dots = Dots()
    moves = Moves(labyrinth, hero, enemy)
    click = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENEMY_EVENT_TYPE:
                moves.move_enemy()
        moves.update_hero()
        dots.make_dots(screen, labyrinth)
        moves.make(screen)
        pygame.display.flip()
        click.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
