import pygame
import random

WIDTH, HEIGHT = 560, 650
TILE_SIZE = 20
FREE_TILES = [1, 5]
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
YELLOW = (245, 208, 51)
YELLOW_FOR_DOTS = (255, 230, 2)
pygame.font.init()


class Pacman:
    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        self.x, self.y = self.start_position(labyrinth)

    def set_position(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def make(self, screen, file):
        image = pygame.image.load(file).convert_alpha()
        static_pacman = pygame.transform.scale(image, (20, 20))
        center = self.x * TILE_SIZE, 25 + self.y * TILE_SIZE
        screen.blit(static_pacman, center)

    def make_as_circle(self, screen):
        # создание пакмана в виде шарика
        center = self.x * TILE_SIZE + TILE_SIZE // 2, 25 + self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, YELLOW_FOR_DOTS, center, TILE_SIZE // 2)

    def start_position(self, labyrinth):
        x = random.randint(1, self.labyrinth.width - 1)
        y = random.randint(1, self.labyrinth.height - 1)
        while labyrinth.get_tile_id((x, y)) not in FREE_TILES:
            x = random.randint(1, self.labyrinth.width - 1)
            y = random.randint(1, self.labyrinth.height - 1)
        return x, y
