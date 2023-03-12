import pygame
import numpy as np


class PokeSprites:
    """Represents a set of pokemon sprites.
    Each piece is an object of the Piece class.
    """

    def __init__(self, poke):
        """Initialize attributes to represent the overall set of pieces."""

        self.poke = poke
        self.sprites = []
        color_key = 'red'
        sheet_file = 'assets/sprites/pokemon-rb.png'
        shiny_file = 'assets/sprites/pokemon-rb.png'
        if poke.gen == 2:
            color_key = 'white'
            if poke.game == 'gold':
                shiny_file = 'assets/sprites/gold-shiny.png'
                sheet_file = 'assets/sprites/gold.png'
            elif poke.game == 'silver':
                shiny_file = 'assets/sprites/silver-shiny.png'
                sheet_file = 'assets/sprites/silver.png'
            else:
                shiny_file = 'assets/sprites/crystal-shiny.png'
                sheet_file = 'assets/sprites/crystal.png'
        elif poke.game == 'yellow':
            color_key = 'white'
            shiny_file = 'assets/sprites/yellow.png'
            sheet_file = 'assets/sprites/yellow.png'
        elif poke.show_color:
            color_key = 'white'
            shiny_file = 'assets/sprites/rb-color.png'
            sheet_file = 'assets/sprites/rb-color.png'

        self.color_key = color_key
        self.poke_ss = SpriteSheet(sheet_file)
        self.poke_ss_shiny = SpriteSheet(shiny_file)
        self._load_sprites(color_key)

    def _load_sprites(self, color_key):
        """Builds the overall set:
        - Loads images from the sprite sheet.
        - Creates a Pokemon object, and sets appropriate attributes
          for that pokemon.
        - Adds each pokemon to the group self.pokemon.
        """
        self.sprites = []
        x = 11
        y = 12
        border_offset = 1
        rect = (x * 57 + 1, y * 57 + 1, 56, 56)

        # Poke 1
        poke_1_rect = rect
        poke_1_image = self.poke_ss.image_at(poke_1_rect, color_key)

        poke_1 = Pokemon(self.poke)
        poke_1.image = poke_1_image
        poke_1.name = 'poke_1'
        self.sprites.append(poke_1)

        fave_x = 540
        fave_x_offset = 60
        fave_y = 440

        # Fave 1
        fave_1_rect = rect
        fave_1_image = self.poke_ss.image_at(fave_1_rect, color_key)

        fave_1 = Pokemon(self.poke)
        fave_1.image = fave_1_image
        fave_1.name = 'fave_1'
        fave_1.x = fave_x + (fave_x_offset * 0)
        fave_1.y = fave_y + border_offset
        self.sprites.append(fave_1)

        # Fave 2
        fave_2_rect = rect
        fave_2_image = self.poke_ss.image_at(fave_2_rect, color_key)

        fave_2 = Pokemon(self.poke)
        fave_2.image = fave_2_image
        fave_2.name = 'fave_2'
        fave_2.x = fave_x + (fave_x_offset * 1)
        fave_2.y = fave_y + border_offset
        self.sprites.append(fave_2)

        # Fave 3
        fave_3_rect = rect
        fave_3_image = self.poke_ss.image_at(fave_3_rect, color_key)

        fave_3 = Pokemon(self.poke)
        fave_3.image = fave_3_image
        fave_3.name = 'fave_3'
        fave_3.x = fave_x + (fave_x_offset * 2)
        fave_3.y = fave_y + border_offset
        self.sprites.append(fave_3)

    def get_image(self, poke, poke_data, big, icon):
        x = 11
        x_mult = 57
        y_mult = 57
        x_off = 1
        y_off = 1
        y = 12
        is_shiny = False
        missing = False

        if poke.gen == 2 or poke.game == 'yellow' or poke.show_color:
            x_off = 0
            y_off = 0
            x_mult = 56
            y_mult = 56
            is_shiny = poke_data['is_shiny'] == 1
        if poke_data['id'] != '0':
            try:
                if poke_data['id'] == '255':
                    raise KeyError
                if poke.gen != 2 and (poke.game == 'yellow' or poke.show_color):
                    id = poke.pokedex[poke_data['id']]['dex']
                    y = np.ceil(id / 16) - 1
                    x = (id % 16)
                    if x == 0:
                        x = 15
                    else:
                        x = x - 1
                else:
                    pokedex = poke.pokedex[poke_data['id']]
                    x = pokedex['tile_x']
                    y = pokedex['tile_y']
            except KeyError:
                missing = True
                if poke.gen == 2:
                    x = 11
                    y = 12
                elif poke.game == 'yellow' or poke.show_color:
                    x = 7
                    y = 9
                else:
                    x = 7
                    y = 12
        if icon:
            rect = (x * x_mult + x_off + 5, y * y_mult + y_off + 5, 35, 35)
        else:
            rect = (x * x_mult + x_off, y * y_mult + y_off, 56, 56)
        if is_shiny:
            image = self.poke_ss_shiny.image_at(rect, self.color_key)
        else:
            image = self.poke_ss.image_at(rect, self.color_key)
        if not missing:
            image = pygame.transform.flip(image, True, False)
        if big:
            image = pygame.transform.scale(image, (170, 170))

        return image

    def update_sprite(self, poke, index, poke_data, big=False):
        image = self.get_image(poke, poke_data, big, False)
        poke.poke_sprites.sprites[index].image = image

    def blank_sprite(self, poke, index):
        x = 8
        x_mult = 57
        y_mult = 57
        x_off = 1
        y_off = 1
        y = 12

        if poke.gen == 2:
            x = 13
            x_off = 0
            y_off = 0
            x_mult = 56
            y_mult = 56
        elif poke.game == 'yellow' or poke.show_color:
            x_off = 0
            y_off = 0
            x_mult = 56
            y_mult = 56
            x = 8
            y = 9
        rect = (x * x_mult + x_off, y * y_mult + y_off, 56, 56)
        image = self.poke_ss.image_at(rect, self.color_key)
        poke.poke_sprites.sprites[index].image = image

    def set_icon(self, poke, id):
        data = {
            "id": id,
            "is_shiny": False
        }
        image = self.get_image(poke, data, False, True)
        pygame.display.set_icon(image)


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Pokemon:
    """Represents a pokemon image."""

    def __init__(self, poke):
        """Initialize attributes to represent a pokemon."""
        self.image = None
        self.name = ''
        self.color = ''

        self.screen = poke.screen

        # Start each piece off at the top left corner.
        self.x, self.y = 20.0, 0.0

    def blitme(self):
        """Draw the piece at its current location."""
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)