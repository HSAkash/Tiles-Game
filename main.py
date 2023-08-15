import pygame
import random
from settings import *
from tiles import Tile
from pygame.sprite import Group

# Tiles game
class TilesGame:
    def __init__(self):
        pygame.init()

        # Set up screen
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False

        # Set up groups
        self.all_sprites = Group()
        self.tiles = Group()

        # Load tiles
        self.load_tiles()


        # Define game states
        self.GAME_STATE_START = "start"
        self.GAME_STATE_PLAYING = "playing"
        self.GAME_STATE_SOLVED = "solved"
        # self.game_state = self.GAME_STATE_PLAYING
        self.game_state = self.GAME_STATE_START


        # Button
        self.start_button = pygame.Rect(
            WINDOW_WIDTH / 2 - 100,
            WINDOW_HEIGHT / 2 - 25,
            BUTTON_WIDTH, BUTTON_HEIGHT)
        
        self.restart_button = pygame.Rect(
            WINDOW_WIDTH / 2 - 100,
            WINDOW_HEIGHT / 2 + 25,
            BUTTON_WIDTH, BUTTON_HEIGHT)

        # Button text
        start_font = pygame.font.SysFont("Arial", 20)
        self.start_text = start_font.render("Start", True, WHITE)
        self.start_text_rect = self.start_text.get_rect(center=self.start_button.center)

        restart_font = pygame.font.SysFont("Arial", 20)
        self.restart_text = restart_font.render("Restart", True, WHITE)
        self.restart_text_rect = self.restart_text.get_rect(center=self.restart_button.center)



    def load_tiles(self):
        # tiles initial positions
        positions = [(i, j) for i in range(ROWS) for j in range(COLS)]
        # shuffle positions
        shuffled_positions = positions.copy()
        random.shuffle(shuffled_positions)
        # create tiles
        index = 1
        for _ in range(ROWS):
            for _ in range(COLS):
                x, y = shuffled_positions.pop()
                self.tiles.add(Tile(self, x, y, index))
                index += 1


    def get_tile(self, row, col):
        for tile in self.tiles:
            if tile.x == row and tile.y == col:
                return tile

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events() 
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                # Start button
                if self.game_state == self.GAME_STATE_START:
                    if self.start_button.collidepoint(x, y):
                        self.start_game()
                # Playing
                elif self.game_state == self.GAME_STATE_PLAYING:
                    # get clicked tile
                    clicked_tile = self.get_clicked_tile(x, y)
                    if clicked_tile:
                        # check if clicked tile is adjacent to empty tile and move it
                        self.move_tile(clicked_tile)
                # Solved
                elif self.game_state == self.GAME_STATE_SOLVED:
                    # Restart button
                    if self.restart_button.collidepoint(x, y):
                        self.restart_game()

    def get_clicked_tile(self, x, y):
        # get clicked tile
        for tile in self.tiles:
            if tile.rect.collidepoint(x, y):
                return tile
        return None

    def move_tile(self, clicked_tile):
        # get empty adjacent tile
        empty_tile = self.get_empty_adjacent_tile(clicked_tile)
        if empty_tile:
            # swap clicked tile and empty tile
            clicked_tile.x, clicked_tile.y , empty_tile.x, empty_tile.y = empty_tile.x, empty_tile.y, clicked_tile.x, clicked_tile.y
            # check if solved after move then update game state
            if self.is_solved():
                self.game_state = self.GAME_STATE_SOLVED


    def get_empty_adjacent_tile(self, tile):
        # Find empty tile
        neighbors = tile.get_neighbors()
        for neighbor in neighbors:
            """
            neighbor.index == ROWS*COLS is the index of the empty tile
            """
            if neighbor and neighbor.index == ROWS*COLS: 
                return neighbor
        return None
    
    def is_solved(self):
        """
        Check if tiles are in order
        0x0 position is the first tile with index 1
        0x1 position is the second tile with index 2
        .....
        """
        for tile in self.tiles:
            if tile.index != tile.x + tile.y *COLS + 1:
                return False
        return True
    
    def solved_display(self):
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Solved!", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.screen.blit(text, text_rect)

        self.restart_button = pygame.draw.rect(self.screen, BUTTON_COLOR, self.restart_button)
        self.screen.blit(self.restart_text, self.restart_text_rect)


    def update(self):
        self.all_sprites.update()

    def start_game(self):
        self.tiles.empty()
        self.all_sprites.empty()
        self.load_tiles()
        self.game_state = self.GAME_STATE_PLAYING

    def restart_game(self):
        self.tiles.empty()
        self.all_sprites.empty()
        self.load_tiles()
        self.game_state = self.GAME_STATE_PLAYING

    def start_display(self):
        self.start_button = pygame.draw.rect(self.screen, BUTTON_COLOR, self.start_button)
        self.screen.blit(self.start_text, self.start_text_rect)

    def draw(self):
        self.screen.fill(WHITE)
        for tile in self.tiles:
            tile.draw(self.screen)

        if self.game_state == self.GAME_STATE_START:
            self.start_display()
        elif self.game_state == self.GAME_STATE_SOLVED:
            self.solved_display()


        pygame.display.update()


if __name__ == "__main__":
    game = TilesGame()
    while game.running:
        game.run()