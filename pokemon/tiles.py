import pygame


class Tiles:
    def __init__(self, filename):
        self.tile_size = (8, 8)
        self.tileset_image = pygame.image.load(filename).convert()
        self.tiles = []
        self.load_tiles()

    def load_tiles(self):
        for y in range(0, self.tileset_image.get_height(), self.tile_size[1]):
            row = []
            for x in range(0, self.tileset_image.get_width(), self.tile_size[0]):
                rect = pygame.Rect(x, y, self.tile_size[0], self.tile_size[1])
                image = pygame.Surface(self.tile_size, pygame.SRCALPHA)
                image.blit(self.tileset_image, (0, 0), rect)
                row.append(image)
            self.tiles.append(row)

    def draw_tile(self, surface, tile_index, x, y, scale=1):
        tile_surface = self.tiles[tile_index[1]][tile_index[0]]
        scaled_size = (int(self.tile_size[0] * scale), int(self.tile_size[1] * scale))
        scaled_surface = pygame.transform.scale(tile_surface, scaled_size)
        surface.blit(scaled_surface, (x, y))

    def draw_border_rect(self, surface, row_index, width, height, x, y, scale=1):
        top_left = (0, row_index)
        top_right = (2, row_index)
        bottom_left = (4, row_index)
        bottom_right = (5, row_index)
        top_side = (1, row_index)
        bottom_side = (1, row_index)
        left_side = (3, row_index)
        right_side = (3, row_index)
        middle = (15, 15)

        # Draw corners
        self.draw_tile(surface, top_left, x, y, scale)
        self.draw_tile(surface, top_right, x + (width - 1) * self.tile_size[0] * scale, y, scale)
        self.draw_tile(surface, bottom_left, x, y + (height - 1) * self.tile_size[1] * scale, scale)
        self.draw_tile(surface, bottom_right, x + (width - 1) * self.tile_size[0] * scale,
                       y + (height - 1) * self.tile_size[1] * scale, scale)

        # Draw sides
        for i in range(1, width - 1):
            self.draw_tile(surface, top_side, x + i * self.tile_size[0] * scale, y, scale)
            self.draw_tile(surface, bottom_side, x + i * self.tile_size[0] * scale,
                           y + (height - 1) * self.tile_size[1] * scale, scale)
        for i in range(1, height - 1):
            self.draw_tile(surface, left_side, x, y + i * self.tile_size[1] * scale, scale)
            self.draw_tile(surface, right_side, x + (width - 1) * self.tile_size[0] * scale,
                           y + i * self.tile_size[1] * scale, scale)

        # Draw middle
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                self.draw_tile(surface, middle, x + i * self.tile_size[0] * scale, y + j * self.tile_size[1] * scale,
                               scale)

