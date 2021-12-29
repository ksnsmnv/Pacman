import pygame


def main():
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)
    # создание экземпляра лабиринта (из текствого файла в матрицу)
    labyrinth = Labyrinth()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # создание самого лабиринта (из матрицы в виджет pygame)
        screen.fill((255, 255, 80))
        labyrinth.make(screen)
        pygame.display.flip()
        clock.tick(15)
    pygame.quit()


class Labyrinth:
    def __init__(self):
        self.map = []
        with open("pacman_light_labyrinth.txt") as text_lab:
            for line in text_lab:
                # создание матрицы со значениями "1", "0", отвечающими за стены и пустые части либиринта
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = 17
        self.free_tiles = [1]

    def make(self, screen):
        # цвета для  каждого символа в лабиринте
        # 0 - стена, 1 - можно ходить, 9 - место за полем, 2 - могут ходить только приведения
        colors = {0: (255, 255, 255), 1: (0, 0, 0), 9: (255, 255, 80), 2: (0, 56, 56)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]


if __name__ == '__main__':
    main()