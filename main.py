import pygame
import random

TILE_SIZE = 20
FREE_TILES = [1, 5]


def main():
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)
    # создание экзепляра лабиринта (из текствого файла в матрицу)
    labyrinth = Labyrinth()
    # создание экземпляра пакмана
    pacman = Pacman(labyrinth)
    # создание экземпляра PacmanMoves, который задает движение пакмана
    pacman_moves = PacmanMoves(labyrinth, pacman)
    # создание экземпляра точек
    dots = Dots()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pacman_moves.change_pos()
        screen.fill((0, 0, 0))
        # создание самого лабиринта (из матрицы в виджет pygame)
        labyrinth.make(screen)
        pacman.make(screen)
        dots.make_dots(screen, labyrinth)
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


class Pacman:
    def __init__(self, labyrinth):
        self.x, self.y = self.start_position(labyrinth)

    def set_position(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def make(self, screen):
        # создание пакмана в виде шарика
        center = self.x * TILE_SIZE + TILE_SIZE // 2, \
                self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (232, 167, 2), center, TILE_SIZE // 2)

    def start_position(self, labyrinth):
        x = random.randint(0, 27)
        y = random.randint(0, 27)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(0, 27)
            y = random.randint(0, 27)
        return x, y


class PacmanMoves:
    def __init__(self, labyrinth, pacman):
        self.labyrinth = labyrinth
        self.pacman = pacman

    def change_pos(self):
        # зменение позиции пакмана
        new_x, new_y = self.pacman.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT] and new_x == 0:
            new_x += 27
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT] and new_x == 27:
            new_x -= 27
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            new_y += 1
        # проверка : свободна ли клетка
        if self.labyrinth.tile_is_free((new_x, new_y)):
            self.pacman.set_position((new_x, new_y))


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


if __name__ == '__main__':
    main()
