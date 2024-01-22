'''Example showing how variables / constants can be used to setup a Pygame program.'''

# Example file showing a basic pygame "game loop"
import pygame

# Constants
WIDTH = 1280
HEIGHT = 720

BG_COLOR = 'purple'
TITLE = 'Fun with Constants and Vars'

# pygame setup
pygame.init()
pygame.display.set_caption(TITLE)

# Variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
