import pygame
from settings import *
from random import choice


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, index) -> None:
        super().__init__(game.all_sprites)

        # Set the tile's attributes
        self.game = game
        self.x = x
        self.y = y
        self.index = index

        # Set the color of the tile
        self.color = TILES_COLOR

        # Set the color of the empty tile
        if self.index == ROWS*COLS:
            self.color = EMPTY_TILE_COLOR

        # Number surface
        self.number_font = pygame.font.SysFont("Arial", 100)
        self.number_text = self.number_font.render(str(self.index), True, WHITE)
        self.number_rect = self.number_text.get_rect()

        self.rect = pygame.Rect(
            TILE_SIZE * self.x + TILES_BORDER_WIDTH,
            TILE_SIZE * self.y +TILES_BORDER_WIDTH,
            TILE_SIZE - 2*TILES_BORDER_WIDTH,
            TILE_SIZE - 2*TILES_BORDER_WIDTH)
        self.number_rect.center = self.rect.center

        self.pos = pygame.math.Vector2(self.x, self.y)


    def update(self) -> None:
        self.rect = pygame.Rect(
            TILE_SIZE * self.x + TILES_BORDER_WIDTH,
            TILE_SIZE * self.y +TILES_BORDER_WIDTH,
            TILE_SIZE - 2*TILES_BORDER_WIDTH,
            TILE_SIZE - 2*TILES_BORDER_WIDTH)
        self.number_rect.center = self.rect.center


    def draw(self, surface: pygame.Surface) -> None:
        # Shadow drawing
        pygame.draw.rect(surface, SHADOW_COLOR, self.rect.move(SHADOW_OFFSET), border_radius=RADIUS)
        # Tile drawing
        pygame.draw.rect(surface, self.color, self.rect, border_radius=RADIUS)
        # Number drawing
        surface.blit(self.number_text, self.number_rect)


    def get_neighbors(self) -> list:
        neighbors = []
        if self.x < COLS - 1:
            neighbors.append(self.game.get_tile(self.x + 1, self.y))
        if self.x > 0:
            neighbors.append(self.game.get_tile(self.x - 1, self.y))
        if self.y < ROWS - 1:
            neighbors.append(self.game.get_tile(self.x, self.y + 1))
        if self.y > 0:
            neighbors.append(self.game.get_tile(self.x, self.y - 1))
        return neighbors



