'''Example showing how a custom config.py module can be used to setup a Pygame program.'''

# Example file showing a basic pygame "game loop"
import pygame
from config import settings

screen_settings = settings['screen']

# pygame setup
pygame.init()
pygame.display.set_caption(settings['title'])

# Variables
screen = pygame.display.set_mode((screen_settings['width'], screen_settings['height']))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(screen_settings['bg_color'])

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
