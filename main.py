import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 15


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    click = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get();
        if event.tyoe == pygame.QUIT:
            running = False
        screen.fill((0, 0, 0))
        pygame.display.filp()
        click.tilck(FPS)