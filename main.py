import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 15
MAPS_DIR = "maps"
TILE_SIZE = 32


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile - finish_tile

    def render(self, screen):
        colors = {0: (0, 0, 0), 1:(120, 120, 120), 2:(50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    labyrinth = Labyrinth('simlpe_map.txt', [0, 2], 2)
    click = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.tyoe == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.filp()
        click.tilck(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()