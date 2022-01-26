import pygame

YELLOW_FOR_DOTS = (255, 230, 2)
TILE_SIZE = 20


class Dots:
    def make_dots(self, screen, labyrinth):
        for i in range(len(labyrinth.map)):
            for j in range(len(labyrinth.map[0])):
                if labyrinth.map[i][j] == 1:
                    center = j * TILE_SIZE + TILE_SIZE // 2, 25 + i * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, YELLOW_FOR_DOTS, center, TILE_SIZE // 6)


class Bonus:
    def __init__(self, score):
        self.all_bonus = 0
        self.score = score

    def make(self, screen, labyrinth):
        for i in range(len(labyrinth.map)):
            for j in range(len(labyrinth.map[0])):
                if labyrinth.map[i][j] == 3:
                    center = j * TILE_SIZE + TILE_SIZE // 2, 25 + i * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, YELLOW_FOR_DOTS, center, TILE_SIZE // 3)
                    self.all_bonus += 1

    def get_bonus(self):
        return self.all_bonus * 50
