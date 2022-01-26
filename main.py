import pygame
import random
import time
from class_labyrinth import Labyrinth
from class_pacman import Pacman


WIDTH, HEIGHT = 560, 650
TILE_SIZE = 20
FREE_TILES = [1, 5]
FREE_TILES_FOR_ENEMY = [1, 2, 5]
ENEMY_EVENT = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
YELLOW = (245, 208, 51)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW_FOR_DOTS = (255, 230, 2)
DARK_BLUE = (0, 0, 80)
GREY = (130, 130, 120)
BLUE_FOR_BORDERS = (0, 0, 120)
WINNING_MESSAGE = ['Congrats!', 'You won!', 'Hurray!', 'Gorgeous!', 'Cool!', 'Amazing!']
LOOSING_MESSAGE = ['You lost!', 'Maybe next time...', 'You can do better!']
ENEMY_START_POS = [(11, 14), (12, 14), (13, 14)]
pygame.font.init()


# создание текстового объекта
def text_objects(text, font, color=WHITE):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# создание конпки с функционалом
def button(msg, x, y, w, h, ic, ac, action=''):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(SCREEN, ac, (x, y, w, h))
        if click[0] == 1 and action:
            if action == 'level1_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 350, (15, 30))
            if action == 'level2_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 250, (10, 25))
            if action == 'level3_1':
                main((560, 650), 'pacman_light_labyrinth.txt', 200, (5, 20))
            if action == 'level1_2':
                main((560, 650), 'pacman_labyrinth.txt', 350, (30, 45))
            if action == 'level2_2':
                main((560, 650), 'pacman_labyrinth.txt', 250, (20, 35))
            if action == 'level3_2':
                main((560, 650), 'pacman_labyrinth.txt', 200, (15, 30))
            elif action == 'quit':
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(SCREEN, ic, (x, y, w, h))

    small_text = pygame.font.Font(None, 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), y + (h / 2))
    SCREEN.blit(text_surf, text_rect)


def game_is_over_message(message, size=115):
    coordinates = ((0, HEIGHT / 6 + 20), (WIDTH, HEIGHT * 3 / 5))
    pygame.draw.rect(SCREEN, WHITE, coordinates)
    text = pygame.font.Font(None, size)
    text_surf, text_rect = text_objects(message, text, DARK_BLUE)
    text_rect.center = ((WIDTH / 2), (HEIGHT / 2))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()


# создание экрана меню
def game_intro():
    pygame.display.set_caption('main menu')
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        SCREEN.fill(DARK_BLUE)

        # --- текст для экрана меню ---
        large_text = pygame.font.Font(None, 115)
        text_surf, text_rect = text_objects("PAC-MAN", large_text, YELLOW)
        text_rect.center = ((WIDTH / 2), (HEIGHT / 4))
        SCREEN.blit(text_surf, text_rect)

        button("Labyrinth 1:", WIDTH / 6, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6, 300, 100, 50, DARK_BLUE, BLACK, 'level1_1')
        button("Level 2", WIDTH / 6, 375, 100, 50, DARK_BLUE, BLACK, 'level2_1')
        button("Level 3", WIDTH / 6, 450, 100, 50, DARK_BLUE, BLACK, 'level3_1')

        button("Labyrinth 2:", WIDTH / 6 * 3.7, 230, 100, 50, DARK_BLUE, DARK_BLUE)
        button("Level 1", WIDTH / 6 * 3.7, 300, 100, 50, DARK_BLUE, BLACK, 'level1_2')
        button("Level 2", WIDTH / 6 * 3.7, 375, 100, 50, DARK_BLUE, BLACK, 'level2_2')
        button("Level 3", WIDTH / 6 * 3.7, 450, 100, 50, DARK_BLUE, BLACK, 'level3_2')

        button("Quit", 220, 520, 100, 50, DARK_BLUE, BLACK, 'quit')
        pygame.display.update()
        pygame.time.Clock().tick(15)


def main(size, file_name, speed, start):
    pygame.display.set_caption('pac-man')
    pygame.init()
    screen = pygame.display.set_mode(size)
    # количество оставшихся жизней на начало игры
    lives_left = 2

    # появление на экране счета игрока
    large_text = pygame.font.Font(None, 24)
    text_surf, text_rect = text_objects("Score:", large_text)
    text_rect.center = ((TILE_SIZE * 5), (TILE_SIZE / 2))
    screen.blit(text_surf, text_rect)

    # количество жизней на начало игры
    message = 'You have ' + str(lives_left + 1) + ' lives left'
    small_text = pygame.font.Font(None, 24)
    text_surf, text_rect = text_objects(message, small_text)
    text_rect.center = (WIDTH // 2, HEIGHT - (TILE_SIZE // 2))
    SCREEN.blit(text_surf, text_rect)

    # счет игрока на начало игры
    score = 0
    # лабиринт (из текствого файла в двумерный список)
    labyrinth = Labyrinth(file_name)
    # пакман
    pacman = Pacman(labyrinth)
    # обычные точки
    dots = Dots()
    # точки-бонусы
    bonus = Bonus(score)
    # приведения
    red_enemy = Enemy(1, speed)
    pink_enemy = Enemy(2, speed)
    orange_enemy = Enemy(3, speed)
    # PacmanMoves задает движение пакмана и приведений
    pacman_moves = PacmanMoves(screen, labyrinth, pacman, score, dots,
                               red_enemy, pink_enemy, orange_enemy, bonus)

    clock = pygame.time.Clock()
    game_over = False
    has_won = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_intro()
            elif event.type == ENEMY_EVENT:
                if pacman_moves.flag2(start):
                    pacman_moves.move_red_enemy()
                if pacman_moves.flag(start):
                    pacman_moves.move_pink_enemy()
                pacman_moves.move_orange_enemy()

        # перемещение пакмана, если игра не закончена
        if not game_over:
            direction = pacman_moves.change_pos(screen)
            if pacman_moves.get_direction(direction) == 'make_a_circle':
                # создание изображений элементов игры
                pacman_moves.make(False)
            else:
                pacman_moves.make(pacman_moves.get_direction(direction))

        # если не осталось жизней, выводится сообщение и через 3 секунды происходит переход к экранк меню
        elif game_over and (not lives_left or has_won):
            if has_won and game_over:
                message = random.choice(WINNING_MESSAGE)
                if len(message) > 13:
                    game_is_over_message(message, HEIGHT // len(message) * 2)
                else:
                    game_is_over_message(message)
            elif game_over:
                message = random.choice(LOOSING_MESSAGE)
                if len(message) > 13:
                    game_is_over_message(message, HEIGHT // len(message) * 2)
                else:
                    game_is_over_message(message)
            time.sleep(3)
            game_intro()

        # если остались жизни, внизу печатается количество жизней и через 2 секунды игра начинается заново
        # при этом съеденные точки заново не появляются
        else:
            if game_over:
                coordinates = ((0, HEIGHT - TILE_SIZE), (WIDTH, HEIGHT))
                pygame.draw.rect(screen, BLACK, coordinates)

                lives_left -= 1
                message = 'You have ' + str(lives_left + 1) + ' lives left'
                small_text = pygame.font.Font(None, 24)
                text_surf, text_rect = text_objects(message, small_text)
                text_rect.center = (WIDTH // 2, HEIGHT - (TILE_SIZE // 2))
                SCREEN.blit(text_surf, text_rect)

                # заново задаем положение пакмана и призраков
                start = pacman.start_position(labyrinth)
                pacman.set_position(start)
                start = red_enemy.start_position(1)
                red_enemy.set_position(start)
                start = orange_enemy.start_position(2)
                orange_enemy.set_position(start)
                start = pink_enemy.start_position(3)
                pink_enemy.set_position(start)
                game_over = False

        # вывод текущего счета на экран
        pacman_moves.change_score(screen)
        # проверка на то, выиграл или проиграл ли игрок
        if pacman_moves.won():
            has_won = True
            game_over = True
        elif pacman_moves.lost(1) or pacman_moves.lost(2) or pacman_moves.lost(3):
            game_over = True
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()

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


class PacmanMoves:
    def __init__(self, screen, labyrinth, pacman, score, dots, red_enemy, pink_enemy, orange_enemy, bonus):
        # инициализация частей программы, которые требуются для выполнения функций этого класса
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

    def move_red_enemy(self):
        # переход к функции find_path_step для получения следующей позиции
        next_position = self.labyrinth.find_path_step(self.enemy1.get_position(),
                                                      self.pacman.get_position())
        self.enemy1.set_position(next_position)

    def move_pink_enemy(self):
        # это привидение следует за клеткой находящийся левее или правее на 4 клетки от пакмана
        position = self.pacman.get_position()
        if self.labyrinth.tile_is_free_for_enemy((position[0], position[1] - 4)):
            next_position = self.labyrinth.find_path_step(self.enemy2.get_position(),
                                                          (position[0], position[1] - 4))
            self.enemy2.set_position(next_position)
        elif self.labyrinth.tile_is_free_for_enemy((position[0] - 4, position[1])):
            next_position = self.labyrinth.find_path_step(self.enemy2.get_position(),
                                                          (position[0] - 4, position[1]))
            self.enemy2.set_position(next_position)

    def move_orange_enemy(self):
        # начинает бежать за нами только когда пакман находится в радиусе 12 клеток
        position = self.pacman.get_position()
        position2 = self.enemy3.get_position()
        if abs(position2[0] - position[0]) <= 12 and abs(position2[1] - position[1]) <= 12:
            next_position = self.labyrinth.find_path_step(position2,
                                                          position)
            self.enemy3.set_position(next_position)
        else:
            step_x = random.randint(0, 27)
            step_y = random.randint(0, 28)
            while not self.labyrinth.tile_is_free_for_enemy((step_x, step_y)):
                step_x = random.randint(0, 27)
                step_y = random.randint(0, 28)
            next_position = self.labyrinth.find_path_step(position2,
                                                          (step_x, step_y))
            self.enemy3.set_position(next_position)

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


class Dots:
    def __init__(self):
        pass

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


if __name__ == '__main__':
    game_intro()
