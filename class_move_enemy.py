import random


class EnemyMoves():
    def __init__(self, red_enemy, pink_enemy, orange_enemy, screen, labyrinth, pacman):
        self.enemy1 = red_enemy
        self.enemy2 = pink_enemy
        self.enemy3 = orange_enemy
        self.screen = screen
        self.labyrinth = labyrinth
        self.pacman = pacman

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
        if abs(position2[0] - position[0]) <= 9 and abs(position2[1] - position[1]) <= 9:
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
