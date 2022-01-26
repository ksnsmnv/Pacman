import pygame

TILE_SIZE = 20
ENEMY_EVENT = 20
ENEMY_START_POS = [(11, 14), (12, 14), (13, 14)]


class Enemy:
    # создание врага, скорость которого задается в меню пакмана
    # чем выше уровень, тем выше скорость
    def __init__(self, number, speed):
        self.x, self.y = self.start_position(number)
        self.speed = speed
        pygame.time.set_timer(ENEMY_EVENT, self.speed)

        # передавание картинок приведений
        if number == 1:
            image = pygame.image.load('red1.jpg').convert_alpha()
            self.new_image = pygame.transform.scale(image, (20, 20))
        elif number == 2:
            image = pygame.image.load('pink1.jpg').convert_alpha()
            self.new_image = pygame.transform.scale(image, (20, 20))
        elif number == 3:
            image = pygame.image.load('orange1.jpg').convert_alpha()
            self.new_image = pygame.transform.scale(image, (20, 20))

    # начальная позиция пакмана
    def start_position(self, number):
        if number == 1:
            return ENEMY_START_POS[0]
        elif number == 2:
            return ENEMY_START_POS[1]
        elif number == 3:
            return ENEMY_START_POS[2]

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def make(self, screen):
        center = self.x * TILE_SIZE, 25 + self.y * TILE_SIZE
        screen.blit(self.new_image, center)