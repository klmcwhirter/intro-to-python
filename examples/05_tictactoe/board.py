'''board.py - the Tic Tac Toe board'''

import logging
from typing import Self

import pygame as pg


class PlayerPiece:
    def __init__(self, name: str, color: str, left_margin: int, **kwargs) -> None:
        self.name = name
        self.color = color
        self.left_margin = left_margin

    def __eq__(self, other: Self | None) -> bool:
        '''Used by detect_winner below'''
        if other is None:
            return False

        return self.name == other.name

    def __str__(self) -> str:
        '''Used by detect_winner below'''
        return self.name

    @staticmethod
    def from_name(name: str, color: str, left_margin: int, **kwargs) -> Self:
        return PlayerPiece(name, color, left_margin, **kwargs)


WAYS_TO_WIN = ((0, 1, 2),
               (3, 4, 5),
               (6, 7, 8),
               (0, 3, 6),
               (1, 4, 7),
               (2, 5, 8),
               (0, 4, 8),
               (2, 4, 6))


class Board:
    def __init__(self, **kwargs) -> None:
        self. _positions: list[PlayerPiece | None]
        self._config = kwargs

        self.width = self._config['screen']['width']
        self.third_width = self.width // 3
        self.two_thirds_width = self.third_width << 1
        self.height = self._config['screen']['height']
        self.third_height = self.height // 3
        self.two_thirds_height = self.third_height << 1

        self.players_font = pg.font.Font(None, self._config['players']['font_size'])
        self.shortcut_font = pg.font.Font(None, self._config['shortcuts']['font_size'])
        self.winner_font = pg.font.Font(None, self._config['winner']['font_size'])

        self.reset()

    def detect_winner(self) -> str | None:
        '''Determines if there is a winner or board is full.'''
        vector = self._positions

        for w2w in WAYS_TO_WIN:
            if vector[w2w[0]] == vector[w2w[1]] == vector[w2w[2]] is not None:
                return str(vector[w2w[0]])

        if len([p for p in vector if p is not None]) >= 9:    # Tie
            return 'Tie'

        return None

    def draw_grid(self, screen: pg.Surface):
        color = self._config['grid']['color']
        self.thickness = self._config['grid']['thickness']

        lines = [
            # Vertical
            ((self.third_width, 0), (self.third_width, self.height)),
            ((self.two_thirds_width, 0), (self.two_thirds_width, self.height)),

            # Horizontal
            ((0, self.third_height), (self.width, self.third_height)),
            ((0, self.two_thirds_height), (self.width, self.two_thirds_height)),
        ]

        for line in lines:
            pg.draw.line(
                screen,
                color,
                line[0],
                line[1],
                width=self.thickness
            )

    def draw_placed(self, screen: pg.Surface) -> None:
        for pos in range(9):
            self._draw_shortcut(screen, pos)
            self._draw_position(screen, pos)

    def _draw_position(self, screen: pg.Surface, pos: int) -> None:
        if self._positions[pos]:
            piece = self._positions[pos]
            player_surf = self.players_font.render(piece.name, True, piece.color)

            player_rect = player_surf.get_rect()

            x, y = self.pos_to_point(pos)
            player_rect.center = ((x * self.third_width) + piece.left_margin, y * self.third_height)
            screen.blit(player_surf, player_rect.center, None)

    def _draw_shortcut(self, screen: pg.Surface, pos: int) -> None:
        surf = self.shortcut_font.render(str(pos), False, self._config['shortcuts']['color'])
        rect = surf.get_rect()

        x, y = self.pos_to_point(pos)
        rect.topleft = ((x * self.third_width) + self.thickness + 2, (y * self.third_height) + self.thickness + 2)

        screen.blit(surf, rect)

    def draw_winner(self, screen: pg.Surface, winner: str) -> None:
        if winner is None:
            return

        winner = f'{winner} WON !' if winner != 'Tie' else 'Tie !'

        surf = self.winner_font.render(
            winner,
            True,
            self._config['winner']['color']
        )

        rect = surf.get_rect()
        rect.center = (self.width / 2, self.height / 2)
        screen.blit(surf, rect)

    def mouse_to_pos(self, mouse_pos: tuple[int, int]) -> int:
        x = 0 if mouse_pos[0] < self.third_width else 1 if mouse_pos[0] < self.two_thirds_width else 2
        y = 0 if mouse_pos[1] < self.third_height else 1 if mouse_pos[1] < self.two_thirds_height else 2
        pos = self.point_to_pos(tuple([x, y]))
        return pos

    def point_to_pos(self, pos: tuple[int, int]) -> int:
        return (pos[1] * 3) + pos[0]

    def pos_to_point(self, pos: int) -> tuple[int, int]:
        return (pos % 3, pos // 3)

    def place_piece(self, pos: int, piece: PlayerPiece) -> tuple[str | None, bool]:
        if not self._positions[pos]:
            x, y = self.pos_to_point(pos)
            logging.debug(f'Position {pos} @ ({x}, {y}) is now occupied by {piece.name}.')
            self._positions[pos] = piece
            return (self.detect_winner(), True)

        logging.warn(f'Position {pos} @ ({x}, {y}) is occupied. Not placing.')
        return (None, False)

    def reset(self) -> None:
        self._positions = [None for _ in range(9)]

    def update(self, screen: pg.Surface, winner: str) -> None:
        self.draw_grid(screen)
        self.draw_placed(screen)
        self.draw_winner(screen, winner)
