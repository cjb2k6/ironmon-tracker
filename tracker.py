import numpy

from json import JSONDecodeError

import json

import sys
import numpy as np

import pygame
import pygame.freetype

from src.pokesprites import PokeSprites
from src.poketypes import PokeTypes
from src.tiles import Tiles


class Poke:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.font = 'assets/pokemon-generation_1_custom.ttf'
        self.XL_FONT = pygame.freetype.Font(self.font, 26)
        self.LG_FONT = pygame.freetype.Font(self.font, 22)
        self.MD_FONT = pygame.freetype.Font(self.font, 20)
        self.GAME_FONT = pygame.freetype.Font(self.font, 18)
        self.NORMAL_FONT = pygame.freetype.Font(self.font, 15)
        self.SM_FONT = pygame.freetype.Font(self.font, 12)
        self.XS_FONT = pygame.freetype.Font(self.font, 8)

        self.bg_color = pygame.Color(248, 248, 248)
        self.WINDOW_X = 800
        self.WINDOW_Y = 500

        try:
            g = open('poke.json')
            self.data = json.load(g)
            g.close()
        except FileNotFoundError:
            self.data = {
                "game": "crystal",
                "gen": 2,
                "frame": 1,
                "team": {
                    "size": 0,
                    "items": [],
                    "view": "lead",
                    "has_starter": 0,
                    "poke1": {
                        "name": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "id": "0",
                        "item": "0",
                        "move_1": "0",
                        "move_2": "0",
                        "move_3": "0",
                        "move_4": "0",
                        "pp_1": "0",
                        "pp_2": "0",
                        "pp_3": "0",
                        "pp_4": "0",
                        "level": 0,
                        "hp": 0,
                        "max_hp": 0,
                        "attack": 0,
                        "defense": 0,
                        "speed": 0,
                        "special_attack": 0,
                        "special_defense": 0,
                        "is_shiny": 0
                    }
                },
                "battleType": "0",
                "enemy": {
                    "id": "0",
                    "level": 0,
                    "types": [],
                    "is_shiny": 0
                }
            }
            g = open('poke.json', 'w')
            g.write(json.dumps(self.data))
            g.close()

        self.game = self.data["game"]

        self.gen = self.data["gen"]

        self.view = "party"

        self.team_size = 0

        self.has_starter = 0

        self.battle_type = "0"

        self.enemy = {"id": "0", "level": 0, "is_shiny": 0}

        m = open('json/decodeCharMap.json')
        self.decode_char_map = json.load(m)

        n = open('json/encodeCharMap.json')
        self.encode_char_map = json.load(n)

        # Load settings, create if does not exist
        try:
            f = open('settings.json')
            self.settings = json.load(f)
            f.close()
        except FileNotFoundError:
            self.settings = {
                "showFavorites": True,
                "favorites": [
                    "1",
                    "4",
                    "7"
                ],
                "showAttempts": True,
                "attempts": 0,
                "rbColor": True,
                "randomMail": False,
                "showMoveBorder": True,
                "borderType": -1
            }
            f = open('settings.json', 'w')
            f.write(json.dumps(self.settings, indent=2))
            f.close()

        # Check if mail file exists, create if not
        try:
            f = open('mail')
            f.close()
        except FileNotFoundError:
            f = open('mail', 'w')
            f.write('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,78,0,0'
                    ',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
            f.close()

        try:
            f = open('json/mail.json')
            self.mail = json.load(f)
            f.close()
        except FileNotFoundError:
            self.mail = [
                          {
                            "line1": "  Back to the   ",
                            "line2": "  lab again!"
                          },
                          {
                            "line1": "  This moveset. ",
                            "line2": "      LMAO"
                          },
                          {
                            "line1": "We ain't gettin' ",
                            "line2": "past the rival."
                          },
                          {
                            "line1": "Yo! We got this!",
                            "line2": "    LET'S GO!"
                          },
                          {
                            "line1": "  This ain't     ",
                            "line2": "  it, Chief."
                          },
                          {
                            "line1": "This is the run.",
                            "line2": "    BELIEVE!"
                          }
                        ]
            f = open('json/mail.json', 'w')
            f.write(json.dumps(self.mail, indent=2))
            f.close()

        self.mail_set = True
        self.mail_initialized = False

        f = open('json/natDexToGen1Map.json')
        self.natDexToGen1Map = json.load(f)
        f.close()

        self.backup_faves = self.settings['favorites']

        if self.gen == 1:
            nat_dex_faves = []
            for fave in self.settings['favorites']:
                try:
                    nat_dex_faves.append(self.natDexToGen1Map[fave])
                except KeyError:
                    nat_dex_faves.append("255")
            self.settings['favorites'] = nat_dex_faves

        self.faves_set = False

        self.show_color = self.settings['rbColor']

        self.screen = pygame.display.set_mode((self.WINDOW_X, self.WINDOW_Y))
        pygame.display.set_caption("IronMON Tracker - Pokémon " + self.game.title() + " Version")

        self.poke_sprites = PokeSprites(self)

        f = open('json/pokedex.json')
        self.pokedex = json.load(f)
        f.close()

        f = open('json/moveList1.json')
        self.move_list = json.load(f)
        f.close()

        f = open('json/items-gen1.json')
        self.items = json.load(f)
        f.close()

        if self.game == 'yellow':
            f = open('json/pokedexy.json')
            self.pokedex = json.load(f)
            f.close()

        if self.gen == 2:
            f = open('json/pokedex2.json')
            self.pokedex = json.load(f)
            f.close()

            f = open('json/moveList2.json')
            self.move_list = json.load(f)
            f.close()

            f = open('json/items-gen2.json')
            self.items = json.load(f)
            f.close()

        self.poke_1_data = self.data["team"]["poke1"]

        self.poke_types = PokeTypes()

        self.tileset = Tiles("assets/sprites/menu-tiles.png")

        self.stat_vals = {
            "stat_x": 556 + 25,
            "stat_num_offset": 100,
            "stat_base_y": -8,
            "stat_y_offset": 30
        }

        self.move_vals = {
            "move_y": 210,
            "move_x": 49,
            "type_x": 331,
            "pp_x": 481,
            "pow_x": 581,
            "acc_x": 685,
            "move_y_offset": 44,
            "type_y_offset": 3
        }

        icon_id = "28"
        if self.gen == 1:
            icon_id = self.natDexToGen1Map[icon_id]
        self.poke_sprites.set_icon(self, icon_id)

    def run_game(self):
        self._update_data()
        self._update_screen()
        clock = pygame.time.Clock()
        """Start the main loop for the game."""
        while True:
            clock.tick(60)
            self._check_events()
            if self.settings['randomMail']:
                if not self.mail_set and self.team_size > 0:
                    self.compose_mail()
                self.handle_mail()
            f = open('poke.json')
            try:
                new_data = json.load(f)
                if new_data['game'] != self.game:
                    self.reset()
                if self.data != new_data:
                    self.data = new_data
                    self._update_data()
                    self._update_screen()
            except JSONDecodeError:
                continue
            f.close()

    def _check_events(self):
        try:
            for event in pygame.event.get():
                pressed_keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                        self.modify_attempts()
                    elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                        self.modify_attempts(False)
                    elif pressed_keys[pygame.K_RCTRL] or pressed_keys[pygame.K_LCTRL]:
                        if pressed_keys[pygame.K_KP0] or pressed_keys[pygame.K_r]:
                            self.modify_attempts()
                            self.reset()
                        elif pressed_keys[pygame.K_s]:
                            self.update_mail_operation('2')
                        elif pressed_keys[pygame.K_m]:
                            self.compose_mail()
                        elif pressed_keys[pygame.K_q]:
                            sys.exit()
        except KeyError:
            print('Invalid Key Press')

    def reset(self):
        self.__init__()
        self._update_data()
        self._draw_tracker()

    def save_settings(self):
        with open("settings.json", "w") as jsonFile:
            settings_to_write = self.settings.copy()
            settings_to_write['favorites'] = self.backup_faves
            json.dump(settings_to_write, jsonFile, indent=2)
        self._update_screen()

    def modify_attempts(self, add=True):
        if self.settings['showAttempts']:
            if add:
                self.settings['attempts'] += 1
            else:
                self.settings['attempts'] -= 1
            if self.settings['attempts'] < 0:
                self.settings['attempts'] = 0
            self.save_settings()

    def handle_mail(self):
        f = open("mail", 'r')
        tokens = f.read().split(',')
        f.close()

        if len(tokens) > 0:
            operation = tokens[0]
            if operation == "3":
                self.save_mail(tokens)

    def update_mail_operation(self, op):
        f = open("mail", 'r')
        tokens = f.read().split(',')
        f.close()

        tokens[0] = op
        output = ",".join(tokens)

        f = open("mail", 'w')
        f.write(output)
        f.close()

    def save_mail(self, tokens):
        break_token = "78"
        decoded_mail = {}
        char_tokens = tokens.copy()
        del char_tokens[0]
        current_line = ''

        count = 0

        # Decode mail
        for token in char_tokens:
            if token == break_token:
                decoded_mail['line1'] = current_line
                current_line = ''
            elif count > 32:
                decoded_mail['line2'] = current_line
                break
            else:
                current_line += self.decode_char_map[token]
            count += 1

        # Write decoded mail to mail.json
        print('Adding new mail: \n' + decoded_mail['line1'] + '\n' + decoded_mail['line2'])
        self.mail.append(decoded_mail)
        with open("json/mail.json", "w") as jsonFile:
            json.dump(self.mail, jsonFile, indent=2)

        # Set mail operation back to "0"
        tokens[0] = '0'
        output = ",".join(tokens)

        f = open("mail", 'w')
        f.write(output)
        f.close()

    def compose_mail(self):
        if len(self.mail) > 0:
            mail = self.mail[np.random.randint(0, len(self.mail))]
            self.send_mail(mail)

    def send_mail(self, mail):
        print('Sending Mail...')
        encoded_message = '1,'
        encoded_message += self.encode_line(mail['line1'])
        encoded_message += ',78,'
        encoded_message += self.encode_line(mail['line2'])
        encoded_message += self.get_signature()

        f = open("mail", "w")
        f.write(encoded_message)
        f.close()

        self.mail_set = True
        print('Mail Sent!')

    def encode_line(self, line: str):
        items = []

        index = 0
        skip_next_chars = 0
        for char in line:
            if skip_next_chars < 1:
                if char == "'":
                    next_char = line[index + 1]
                    if next_char == "'":
                        items.append(self.encode_char_map["''"])
                        skip_next_chars = 1
                    elif next_char == "d":
                        items.append(self.encode_char_map["'d"])
                        skip_next_chars = 1
                    elif next_char == "l":
                        items.append(self.encode_char_map["'l"])
                        skip_next_chars = 1
                    elif next_char == "s":
                        items.append(self.encode_char_map["'s"])
                        skip_next_chars = 1
                    elif next_char == "t":
                        items.append(self.encode_char_map["'t"])
                        skip_next_chars = 1
                    elif next_char == "v":
                        items.append(self.encode_char_map["'v"])
                        skip_next_chars = 1
                    elif next_char == "r":
                        items.append(self.encode_char_map["'r"])
                        skip_next_chars = 1
                    elif next_char == "m":
                        items.append(self.encode_char_map["'m"])
                        skip_next_chars = 1
                    else:
                        items.append(self.encode_char_map[char])
                elif char == '~':
                    count = 1
                    key = '~'
                    while line[index + count] != '`':
                        key += line[index + count]
                        count += 1
                    key += '`'
                    items.append(self.encode_char_map[key])
                    skip_next_chars = count

                else:
                    items.append(self.encode_char_map[char])
            else:
                skip_next_chars -= 1
            index += 1

        while len(items) < 16:
            items.append('127')

        new_line = ','.join([str(x) for x in items])

        return new_line

    def get_signature(self):
        return ',' + ','.join([str(x) for x in self.data['team']['poke1']['name']])

    def get_attempts(self):
        return "Attempt: " + str(self.settings['attempts'])

    def _update_screen(self):
        self._draw_tracker()

    def _draw_tracker(self):
        self.screen.fill(self.bg_color)

        for sprite in self.poke_sprites.sprites:
            sprite.blitme()

        if self.team_size > 0:
            self.draw_pokemon_info()

        self.draw_pokemon_stats()
        self.draw_pokemon_moves()
        self.draw_attempts()

        pygame.display.flip()

    def draw_pokemon_info(self):
        main_x = 228

        # Type
        text_surface, rect = self.NORMAL_FONT.render(self.get_type(self.poke_1_data), (0, 0, 0))
        text_rect = text_surface.get_rect(center=(110, 180))
        self.screen.blit(text_surface, text_rect)

        # Name
        self.draw_text(self.decode_poke_name(self.poke_1_data), self.XL_FONT, main_x, 20 + (81 * 0))

        info_base_y = 52
        info_offset_y = 30

        # Level
        self.draw_text(self.get_level(self.poke_1_data), self.GAME_FONT, main_x, info_base_y + (81 * 0))

        # Evolves
        evo = self.pokedex[self.poke_1_data['id']]['evolves_at']
        self.draw_text('Evo: ' + evo, self.GAME_FONT, main_x + 100, info_base_y + (81 * 0))

        # HP
        self.draw_text(self.get_hp(self.poke_1_data), self.GAME_FONT, main_x, info_base_y + (info_offset_y * 1) +
                       (81 * 0))

        # Learned Moves
        self.draw_text(self.get_learned_moves(self.poke_1_data) + " " + self.get_next_move(self.poke_1_data),
                       self.GAME_FONT, main_x, info_base_y + (info_offset_y * 2) + (81 * 0))

        # Heals in Bag
        self.draw_text("Bag Heals: " + self.get_heals(self.poke_1_data), self.GAME_FONT, main_x, info_base_y
                       + (info_offset_y * 3) + (81 * 0))

        # Held Item
        if self.gen == 2:
            item = self.items[self.poke_1_data['item']]['name'].upper()
            self.draw_text('Held: ' + item, self.GAME_FONT, main_x, info_base_y + (info_offset_y * 4) + (81 * 0))

    def draw_pokemon_stats(self):
        self.draw_stat('Atk:', 'attack', 1)
        self.draw_stat('Def:', 'defense', 2)

        if self.gen == 2:
            self.draw_stat('SpAtk:', 'special_attack', 3)
            self.draw_stat('SpDef:', 'special_defense', 4)
            self.draw_stat('Spd:', 'speed', 5)
            self.draw_stat('BST:', 'bst', 6)

        else:
            self.draw_stat('Spd:', 'speed', 3)
            self.draw_stat('Spcl:', 'special_attack', 4)
            self.draw_stat('BST:', 'bst', 5)

    def draw_stat(self, title, stat, position):
        self.draw_text(title, self.GAME_FONT, self.stat_vals['stat_x'],
                       self.stat_vals['stat_base_y'] + (self.stat_vals['stat_y_offset'] * position) + (81 * 0))
        if stat == 'bst':
            text = self.get_bst(self.poke_1_data)
        else:
            text = self.get_stat(self.poke_1_data, stat)
        self.draw_text(text, self.GAME_FONT, self.stat_vals['stat_x'] + self.stat_vals['stat_num_offset'],
                       self.stat_vals['stat_base_y'] + (self.stat_vals['stat_y_offset'] * position + (81 * 0)))

    def draw_pokemon_moves(self):
        # Draw Move Border
        if self.settings['showMoveBorder']:
            if self.settings['borderType'] < 0 or self.settings['borderType'] > 8:
                self.tileset.draw_border_rect(self.screen, int(self.data["frame"]), 33, 9, self.move_vals["move_x"]
                                              - 42, self.move_vals["move_y"] + 6, 3)
            else:
                self.tileset.draw_border_rect(self.screen, self.settings['borderType'], 33, 9, self.move_vals["move_x"]
                                              - 42, self.move_vals["move_y"] + 6, 3)

        # Draw Move Table Headings
        self.draw_move_title('Move', 'move_x')
        self.draw_move_title('Type', 'type_x')
        self.draw_move_title('PP', 'pp_x')
        self.draw_move_title('Pow', 'pow_x')
        self.draw_move_title('Acc', 'acc_x')

        # Draw Moves
        self.draw_move('move_1', 1)
        self.draw_move('move_2', 2)
        self.draw_move('move_3', 3)
        self.draw_move('move_4', 4)

        if int(self.battle_type) > 0 and self.pokedex[self.enemy['id']]['name'] != "":
            text_surface, rect = self.LG_FONT.render(
                self.poke_types.get_multiplier_char(
                    self.enemy['types'],
                    self.move_list[self.poke_1_data['move_1']]), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"] - 20, self.move_vals["move_y"] + 2 +
                                            (self.move_vals["move_y_offset"] * 1) + (81 * 0)))
            text_surface, rect = self.LG_FONT.render(
                self.poke_types.get_multiplier_char(
                    self.enemy['types'],
                    self.move_list[self.poke_1_data['move_2']]), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"] - 20, self.move_vals["move_y"] + 2 +
                                            (self.move_vals["move_y_offset"] * 2) + (81 * 0)))
            text_surface, rect = self.LG_FONT.render(
                self.poke_types.get_multiplier_char(
                    self.enemy['types'],
                    self.move_list[self.poke_1_data['move_3']]), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"] - 20, self.move_vals["move_y"] + 2 +
                                            (self.move_vals["move_y_offset"] * 3) + (81 * 0)))
            text_surface, rect = self.LG_FONT.render(
                self.poke_types.get_multiplier_char(
                    self.enemy['types'],
                    self.move_list[self.poke_1_data['move_4']]), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"] - 20, self.move_vals["move_y"] + 2 +
                                            (self.move_vals["move_y_offset"] * 4) + (81 * 0)))

    def draw_move_title(self, title, x_index):
        text_surface, rect = self.XL_FONT.render(title, (0, 0, 0))
        box_surface = pygame.Surface(text_surface.get_rect().inflate(10, 10).size)
        box_surface.fill(self.bg_color)
        box_surface.blit(text_surface, text_surface.get_rect(center=box_surface.get_rect().center))
        self.screen.blit(box_surface, (self.move_vals[x_index] - 5, self.move_vals["move_y"] + (81 * 0)))

    def draw_move(self, move, position):
        move_data = self.get_move(self.poke_1_data[move])
        y = self.move_vals["move_y"] + (self.move_vals["move_y_offset"] * position) + (81 * 0)

        self.draw_text(move_data['name'].upper(), self.LG_FONT, self.move_vals["move_x"], y)
        self.draw_text(move_data['type'].upper(), self.GAME_FONT, self.move_vals["type_x"], y)
        self.draw_text(self.poke_1_data['pp_' + str(position)], self.LG_FONT, self.move_vals["pp_x"], y)
        self.draw_text(move_data['power'].upper(), self.LG_FONT, self.move_vals["pow_x"], y)
        self.draw_text(move_data['acc'].upper(), self.LG_FONT, self.move_vals["acc_x"], y)

    def draw_attempts(self):
        attempts_y = 412
        fav_x_offset = 350  # about tree fiddy

        # Attempts and Favorites
        if self.battle_type == "0":
            if self.settings["showAttempts"]:
                text_surface, rect = self.MD_FONT.render(self.get_attempts(), (0, 0, 0))
                self.screen.blit(text_surface, (self.move_vals["move_x"], attempts_y +
                                                (self.move_vals["move_y_offset"] * 1) + (81 * 0)))

            if self.settings["showFavorites"]:
                text_surface, rect = self.MD_FONT.render("Favorites: ", (0, 0, 0))
                self.screen.blit(text_surface, (self.move_vals["move_x"] + fav_x_offset, attempts_y +
                                                (self.move_vals["move_y_offset"] * 1) + (81 * 0)))
        else:
            enemy_y = attempts_y - 22
            # Enemy Poke
            text_surface, rect = self.SM_FONT.render("Enemy:", (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"], enemy_y + (self.move_vals["move_y_offset"] * 1)
                                            + (81 * 0)))

            text_surface, rect = self.MD_FONT.render(self.get_enemy(), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"], enemy_y + 20 + (self.move_vals["move_y_offset"]
                                                                                      * 1) + (81 * 0)))

            text_surface, rect = self.MD_FONT.render(self.get_wild(), (0, 0, 0))
            self.screen.blit(text_surface, (self.move_vals["move_x"], enemy_y + 40 + (self.move_vals["move_y_offset"]
                                                                                      * 1) + (81 * 0)))

    def draw_text(self, text, font, x, y):
        text_surface, rect = font.render(text, (0, 0, 0))
        self.screen.blit(text_surface, (x, y))

    def decode_poke_name(self, poke_data):
        name_array = poke_data['name']
        if poke_data['id'] == "255" or poke_data['id'] == "0":
            return ''
        if name_array[0] == 0:
            return self.pokedex[poke_data['id']]['name']
        name = ""
        for x in name_array:
            if x == 80:
                break
            name = name + self.decode_char_map[str(x)]
        return name

    def get_level(self, poke_data):
        if poke_data['id'] == "255" or poke_data['id'] == "0":
            return ''
        return "Lv: " + str(poke_data["level"])

    def get_bst(self, poke_data):
        return str(self.pokedex[poke_data['id']]['bst'])

    def get_type(self, poke_data):
        types = self.pokedex[poke_data['id']]['types']

        if len(types) == 2:
            return str(types[0]).upper() + ' ' + str(types[1]).upper()
        return str(types[0]).upper()

    def get_stat(self, poke_data, key):
        return str(poke_data[key])

    def get_heals(self, poke_data):
        items = self.data['team']['items']
        total_hp = 0
        total_heals = 0

        for item in items:
            try:
                hp = self.items[item['item']]['heal']
            except KeyError:
                hp = 0

            if hp != 0:
                qty = item['qty']
                total_heals += qty
                if hp <= 1:
                    total_hp += poke_data['max_hp'] * hp * qty
                else:
                    if hp > poke_data['max_hp']:
                        hp = poke_data['max_hp']
                    total_hp += hp * qty
        if poke_data['max_hp'] < 1:
            percentage = 0
        else:
            percentage = numpy.round(total_hp / poke_data['max_hp'] * 100)
        return str(int(percentage)) + "%HP (" + str(total_heals) + ")"

    def get_learned_moves(self, poke_data):
        count_learned = 0
        total_moves = 0
        level = poke_data['level']
        moves = self.pokedex[poke_data['id']]['learns_at']
        for move in moves:
            total_moves += 1
            if move <= level:
                count_learned += 1
        return 'Moves: ' + str(count_learned) + '/' + str(total_moves)

    def get_next_move(self, poke_data):
        level = poke_data['level']
        moves = self.pokedex[poke_data['id']]['learns_at']
        for move in moves:
            if move > level:
                return "(" + str(move) + ")"
        return ''

    def get_move(self, move_id):
        try:
            return self.move_list[move_id]
        except KeyError:
            return 'Error: ' + move_id

    def get_enemy(self):
        try:
            name = self.pokedex[self.enemy['id']]['name'].upper()
            type = self.get_type(self.enemy)
        except KeyError:
            return ""
        if self.battle_type == "0" or name == "":
            return ""
        return name + "   Lv: " + str(self.enemy['level']) + "   BST: " \
               + str(self.pokedex[self.enemy['id']]['bst']) + "   " + type

    def get_favorites(self):
        return "Favorites: "

    def get_wild(self):
        if self.battle_type != "1":
            return ""
        moves_learned = self.get_next_move(self.enemy)
        learned_moves = self.get_learned_moves(self.enemy)
        evo = 'Evo: ' + self.pokedex[self.enemy['id']]['evolves_at']
        return learned_moves + '  ' + moves_learned + '  ' + evo

    def get_stats(self, poke_data):
        if poke_data['id'] == "255" or poke_data['id'] == "0":
            return ''
        if self.gen == 2:
            return "Atk: " + str(poke_data["attack"]) + " " + "Def: " + str(
                poke_data["defense"]) + " " + "SpAtk: " + str(poke_data["special_attack"]) + " " + "SpDef: " + str(
                poke_data["special_defense"]) + " " + "Spd: " + str(poke_data["speed"])
        return "Atk: " + str(poke_data["attack"]) + " " + "Def: " + str(poke_data["defense"]) + " " + "Spd: " + str(
            poke_data["speed"]) + " " + "Spc: " + str(poke_data["special"])

    def get_hp(self, poke_data):
        if poke_data['id'] == "255" or poke_data['id'] == "0":
            return ''
        return "HP: " + str(poke_data["hp"]) + " / " + str(poke_data["max_hp"])

    def _update_data(self):
        self.team_size = self.data["team"]["size"]

        if self.gen == 2 and not self.mail_initialized:
            self.has_starter = self.data["team"]["has_starter"]
            if self.has_starter > 0 and self.mail_set:
                self.mail_set = False
                self.mail_initialized = True

        self.enemy = self.data["enemy"]

        self.battle_type = self.data["battleType"]

        if "view" in self.data["team"]:
            self.view = self.data["team"]["view"]

        self.poke_1_data = self.data["team"]["poke1"]

        if self.settings["showFavorites"] and self.battle_type == "0":
            self.poke_sprites.update_sprite(self, 1, {"id": self.settings["favorites"][0], "is_shiny": 0})
            self.poke_sprites.update_sprite(self, 2, {"id": self.settings["favorites"][1], "is_shiny": 0})
            self.poke_sprites.update_sprite(self, 3, {"id": self.settings["favorites"][2], "is_shiny": 0})
        else:
            self.poke_sprites.blank_sprite(self, 1)
            self.poke_sprites.blank_sprite(self, 2)
            self.poke_sprites.blank_sprite(self, 3)

        if self.team_size > 0:
            self.poke_sprites.update_sprite(poke, 0, self.poke_1_data, True)
        else:
            self.poke_sprites.blank_sprite(poke, 0)


if __name__ == '__main__':
    poke = Poke()
    poke.run_game()
