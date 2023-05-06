import pygame

from src.tiles import Tiles


class Menu:
    def __init__(self, tiles, screen, bg_color, font, width, height, x, y, scale, settings, dex):
        self.tiles: Tiles = tiles
        self.screen = screen
        self.bg_color = bg_color
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.scale = scale
        self.settings = settings
        self.options = []

        self.index = 0

        self.option_start_y = 30
        self.option_x_offset = 30
        self.option_y_offset = 55

        bool_dict = {
            True: 'ON',
            False: 'OFF'
        }

        frame_dict = {
            -1: 'FROM GAME',
            0: 'TYPE 0',
            1: 'TYPE 1',
            2: 'TYPE 2',
            3: 'TYPE 3',
            4: 'TYPE 4',
            5: 'TYPE 5',
            6: 'TYPE 6',
            7: 'TYPE 7',
            8: 'TYPE 8',
        }
        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 0), 'SHOW ATTEMPTS', bool_dict, 'showAttempts',
                       settings['showAttempts'], 'boolean')
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 1), 'SHOW FAVORITES', bool_dict, 'showFavorites',
                       settings['showFavorites'], 'boolean')
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 2), 'FAVORITE 1', dex, 'favorites',
                       settings['favorites'][0], 'dex', 0, 255, 0)
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 3), 'FAVORITE 2', dex, 'favorites',
                       settings['favorites'][1], 'dex', 0, 255, 1)
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 4), 'FAVORITE 3', dex, 'favorites',
                       settings['favorites'][2], 'dex', 0, 255, 2)
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 5), 'RB COLOR', bool_dict, 'rbColor',
                       settings['rbColor'], 'boolean')
        )

        self.options.append(
            MenuOption(self.tiles, self.screen, self.bg_color, self.font, width, height, x + self.option_x_offset,
                       self.option_start_y + (self.option_y_offset * 6), 'FRAME', frame_dict, 'borderType',
                       settings['borderType'], 'number', -1, 8)
        )
        self.set_selected_option()

    def draw_border(self, frame):
        self.tiles.draw_border_rect(self.screen, frame, self.width, self.height, self.x, self.y, self.scale)

    def draw_options(self):
        for option in self.options:
            option.draw()

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

    def increment_selected_option(self):
        option = self.options[self.index]
        option.change_data()
        if option.data_type == 'dex':
            self.settings[option.setting][option.fave_index] = option.data
        else:
            self.settings[option.setting] = option.data

    def decrement_selected_option(self):
        option = self.options[self.index]
        option.change_data(-1)
        if option.data_type == 'dex':
            self.settings[option.setting][option.fave_index] = option.data
        else:
            self.settings[option.setting] = option.data


class MenuOption:
    def __init__(self, tiles, screen, bg_color, font, width, height, x, y, title, value_dict, setting, data,
                 data_type='number', min_val=0, max_val=255, fave_index=-1):
        self.tiles = tiles
        self.screen = screen
        self.bg_color = bg_color
        self.font = font
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.title = title
        self.value_dict = value_dict
        self.setting = setting
        self.data = data
        self.data_type = data_type
        self.min = min_val
        self.max = max_val
        self.fave_index = fave_index
        self.rect = pygame.draw.rect(self.screen, self.bg_color, (x, y, width, height))

        self.is_selected = False

    def change_data(self, factor=1):
        if self.data_type == 'number':
            self.data = self.data + (1 * factor)
            if self.data > self.max:
                self.data = self.min
            elif self.data < self.min:
                self.data = self.max
        elif self.data_type == 'dex':
            data = int(self.data) + (1 * factor)
            if data > self.max:
                data = self.min
            elif data < self.min:
                data = self.max
            self.data = str(data)
        elif self.data_type == 'boolean':
            self.data = not self.data

    def set_selected(self, is_selected):
        self.is_selected = is_selected

    def draw(self):
        if self.is_selected:
            self.tiles.draw_tile(self.screen, (3, 9), self.x - 4, self.y - 1, 3)

        # Draw Title
        text_surface, rect = self.font.render(self.title, (0, 0, 0))
        self.screen.blit(text_surface, (self.x + 21, self.y))

        # Draw Value
        if self.data_type == 'dex':
            try:
                value = self.value_dict[self.data]['name'].upper()
                if value == '':
                    value = 'MISSINGNO'
            except KeyError:
                value = 'MISSINGNO'
        else:
            value = self.value_dict[self.data]
        text_surface, rect = self.font.render(':' + value, (0, 0, 0))
        self.screen.blit(text_surface, (self.x + 108, self.y + 25))
