'''game.py - game driver'''

import logging
import os
from pprint import pformat

import pygame as pg

from .board import Board, PlayerPiece

# Setup logging format for the app
logging.basicConfig(level=logging.DEBUG, format='{asctime} - {module} - {funcName} - {levelname} - {message}', style='{')

# initialize pygame
pg.init()

if not pg.font:
    logging.warn('Pygame: Fonts not available')
if not pg.mixer:
    logging.warn('Pygame: Sound not available')


class Game:
    def __init__(self) -> None:
        from .config import settings
        self.config = settings
        logging.debug(pformat(self.config, sort_dicts=False))

        self.width = self.config['screen']['width']
        self.height = self.config['screen']['height']

        basedir = os.path.dirname(__file__)
        self.snd_error = pg.mixer.Sound(os.path.join(basedir, self.config['players']['snd_error']))
        self.snd_placed = pg.mixer.Sound(os.path.join(basedir, self.config['players']['snd_placed']))
        self.snd_winner = pg.mixer.Sound(os.path.join(basedir, self.config['players']['snd_winner']))
        self.snd_winner.set_volume(0.5)

        self.set_window_title()
        self.screen = pg.display.set_mode((self.width, self.height))

        self._board = Board(**self.config)

    def set_window_title(self, addon: str | None = None) -> None:
        msg = self.config['title'] if addon is None else f'{self.config['title']} - {addon}'
        pg.display.set_caption(msg)

    def toggle_player(self, player: str) -> str:
        return 'X' if player == 'O' else 'O'

    def run(self) -> None:
        player: str
        winner: str | None

        def reset():
            nonlocal player, winner
            player = 'X'
            winner = None
            self._board.reset()

        try:
            reset()
            clock = pg.time.Clock()

            running = True
            while running:
                self.set_window_title(f'Next up: {player}' if winner is None else None)

                # poll for events
                # pg.QUIT event means the user clicked X to close your window
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        running = False

                    if winner is None:
                        pos = None

                        if event.type == pg.MOUSEBUTTONUP:
                            pos = self._board.mouse_to_pos(event.pos)
                        elif event.type == pg.KEYDOWN and event.key in range(pg.K_0, pg.K_9 + 1):
                            pos = event.key - pg.K_0

                        if pos is not None:
                            player_config = self.config['players'][player]
                            winner, placed = self._board.place_piece(
                                pos,
                                PlayerPiece.from_name(
                                    player,
                                    player_config['color'],
                                    player_config['left_margin'],
                                    **self.config
                                )
                            )

                            if placed:
                                self.snd_placed.play()
                                player = self.toggle_player(player)
                                if winner:
                                    self.snd_winner.play()
                            else:
                                self.snd_error.play()

                    else:  # have winner
                        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                            reset()

                # fill the screen with a color to wipe away anything from last frame
                self.screen.fill(self.config['screen']['bg_color'])

                # RENDER YOUR GAME HERE
                self._board.update(self.screen, winner)

                # flip() the display to put your work on screen
                pg.display.flip()

                clock.tick(60)  # limits FPS to 60
        finally:
            pg.quit()
