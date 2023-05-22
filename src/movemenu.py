import pygame

from src.tiles import Tiles


class MoveMenu:
    def __init__(self, tiles, screen, bg_color, font, width, height, x, y, scale, moves):
        self.tiles: Tiles = tiles
        self.screen = screen
        self.bg_color = bg_color
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.scale = scale
        self.options = []

        self.index = 0

        self.option_start_y = y + 30
        self.option_x_offset = 30
        self.option_y_offset = 25

        self.opt_width = width * 20

        move_index = 0
        x_offset = self.option_x_offset
        for move in moves:
            if move_index > 6:
                move_index = 0
                x_offset = self.option_x_offset + 180
            self.options.append(
                MoveOption(self.tiles, self.screen, self.bg_color, self.font, self.opt_width, self.option_y_offset,
                           x + x_offset, self.option_start_y + (self.option_y_offset * move_index),
                           move["number"], move["data"], move["level"]
                           )
            )
            move_index = move_index + 1

    def draw_border(self, frame):
        self.tiles.draw_border_rect(self.screen, frame, self.width, self.height, self.x, self.y, self.scale)

    def draw_options(self, current_level):
        for option in self.options:
            option.draw(current_level)

    def next_option(self):
        self.index = self.index + 1
        if self.index >= len(self.options):
            self.index = 0
        self.set_selected_option()

    def prev_option(self):
        self.index = self.index - 1
        if self.index < 0:
            self.index = len(self.options) - 1
        self.set_selected_option()

    def set_selected_option(self):
        index = 0
        for option in self.options:
            option.set_selected(index == self.index)
            index = index + 1

    def check_mouse_hover(self):
        for option in self.options:
            option.set_hovered(option.is_mouse_over())


class MoveOption:
    def __init__(self, tiles, screen, bg_color, font, width, height, x, y, move_number, move_data, move_level):
        self.tiles = tiles
        self.screen = screen
        self.bg_color = bg_color
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.move_number = move_number
        self.move_data = move_data
        self.move_level = move_level
        self.rect = pygame.draw.rect(self.screen, self.bg_color, (x, y, width - 190, height))

        self.is_selected = False
        self.is_hovered = False

    def set_selected(self, is_selected):
        self.is_selected = is_selected

    def set_hovered(self, is_hovered):
        self.is_hovered = is_hovered

    def draw(self, current_level):
        if self.is_selected:
            self.tiles.draw_tile(self.screen, (3, 9), self.x - 4, self.y - 1, 3)
        name = '???'

        if current_level >= self.move_level:
            name = self.move_data["name"].upper()

        # Draw Level
        text_surface, rect = self.font.render(str(self.move_level), (0, 0, 0))
        level_rect = text_surface.get_rect()
        level_rect.topright = (self.x + 20, self.y)
        self.screen.blit(text_surface, level_rect)

        # Draw Name
        text_surface, rect = self.font.render(name, (0, 0, 0))
        self.screen.blit(text_surface, (self.x + 30, self.y))

    def draw_tooltip(self, frame):
        x = self.x + 230
        y = self.y - 90
        width = 10
        height = 8
        self.draw_tooltip_border(frame, width, height, x, y, 3)

    def draw_tooltip_border(self, frame, width, height, x, y, scale):
        self.tiles.draw_border_rect(self.screen, frame, width, height, x - 100, y + 100, scale)

    def is_mouse_over(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

