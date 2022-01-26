import pygame

WIDTH, HEIGHT = 560, 650
TILE_SIZE = 20
FREE_TILES = [1, 5]
WINNING_MESSAGE = ['Congrats!', 'You won!', 'Hurray!', 'Gorgeous!', 'Cool!', 'Amazing!']
LOOSING_MESSAGE = ['You lost!', 'Maybe next time...', 'You can do better!']
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PacmanMoves:
    def __init__(self, screen, labyrinth, pacman, score, dots, bonus,  red_enemy, pink_enemy, orange_enemy):
        # инициализация частей программы, которые требуются для выполнения функций этого класс
        self.enemy1 = red_enemy
        self.enemy2 = pink_enemy
        self.enemy3 = orange_enemy
        self.screen = screen
        self.labyrinth = labyrinth
        self.pacman = pacman
        self.score = score
        self.dots = dots
        self.bonus = bonus
        self.points = 0
        self.direction = 'no'

    # создание всех частей лабиринта в одной функции
    def make(self, file):
        self.labyrinth.make(self.screen)
        if file:
            self.pacman.make(self.screen, file)
        else:
            self.pacman.make_as_circle(self.screen)
        self.dots.make_dots(self.screen, self.labyrinth)
        self.enemy1.make(self.screen)
        self.enemy2.make(self.screen)
        self.enemy3.make(self.screen)
        self.bonus.make(self.screen, self.labyrinth)

    # изменение позиции пакмана
    def change_pos(self, screen):
        new_x, new_y = self.pacman.get_position()
        # --- проверка нажатия клавиш ---
        # для левой клавиши
        if pygame.key.get_pressed()[pygame.K_LEFT] and new_x == 0:
            new_x += 27
            self.direction = 'left'
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            new_x -= 1
            self.direction = 'left'
            # если эта точка имеет "точку", выполняется функция "plus_point"
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
                self.points += 1
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для правой клавиши
        if pygame.key.get_pressed()[pygame.K_RIGHT] and new_x == 27:
            new_x -= 27
            self.direction = 'right'
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            new_x += 1
            self.direction = 'right'
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для верхней клавиши
        if pygame.key.get_pressed()[pygame.K_UP]:
            new_y -= 1
            self.direction = 'up'
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # для нижней клавиши
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            new_y += 1
            self.direction = 'down'
            if self.labyrinth.get_tile_id((new_x, new_y)) == 1:
                self.plus_point(screen, new_x, new_y)
            elif self.labyrinth.get_tile_id((new_x, new_y)) == 3:
                self.plus_bonus(screen, new_x, new_y)
        # проверка : свободна ли клетка
        if self.labyrinth.tile_is_free((new_x, new_y)):
            self.pacman.set_position((new_x, new_y))
        return self.direction

    # прибавляется 10 очков к "score" и стирается точка
    def plus_point(self, screen, new_x, new_y):
        self.labyrinth.map[new_y][new_x] = 5
        self.score += 10
        center = new_x * TILE_SIZE + TILE_SIZE // 2, 25 + new_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, BLACK, center, TILE_SIZE // 2)

    def plus_bonus(self, screen, new_x, new_y):
        self.labyrinth.map[new_y][new_x] = 5
        self.score += 50
        center = new_x * TILE_SIZE + TILE_SIZE // 2, 25 + new_y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, BLACK, center, TILE_SIZE // 2)

    # флаг для активации второго приведения
    def flag(self, start):
        if self.points >= start[0]:
            return True

    # флаг для активации первого приведения
    def flag2(self, start):
        if self.points >= start[1]:
            return True

    # проверка: закончились ли точки
    def won(self):
        if self.labyrinth.maximum_score == 0:
            return True

    # проверка: столкнулся ли пакман с приведением
    def lost(self, number_of_ghost):
        if number_of_ghost == 1:
            return self.pacman.get_position() == self.enemy1.get_position()
        if number_of_ghost == 2:
            return self.pacman.get_position() == self.enemy2.get_position()
        if number_of_ghost == 3:
            return self.pacman.get_position() == self.enemy3.get_position()

        # изменение счета на экране
    def change_score(self, screen):
        large_text = pygame.font.Font(None, 24)
        text_surf, text_rect = self.text_objects(str(self.score), large_text)
        text_rect.center = ((TILE_SIZE * 9), (TILE_SIZE / 2))
        coordinates = ((TILE_SIZE * 7, 0), (TILE_SIZE * 10, TILE_SIZE * 1.5))
        pygame.draw.rect(screen, BLACK, coordinates)
        screen.blit(text_surf, text_rect)

    def text_objects(self, text, font, color=WHITE):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def get_direction(self, direction):
        if direction == 'right':
            return 'pac_man_to_right.gif'
        elif direction == 'left':
            return 'pac_man_to_left.gif'
        elif direction == 'up':
            return 'pac_man_to_top.gif'
        elif direction == 'down':
            return 'pac_man_to_buttom.gif'
        else:
            return 'make_a_circle'
