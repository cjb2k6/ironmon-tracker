from json import JSONDecodeError

from pygame import K_KP0, K_RCTRL, K_LCTRL, K_s, K_m, K_r

import json

import sys
import numpy as np

import pygame
import pygame.freetype


class Poke:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.font = 'pokemon_generation_1.ttf'
        self.XL_FONT = pygame.freetype.Font(self.font, 26)
        self.LG_FONT = pygame.freetype.Font(self.font, 22)
        self.MD_FONT = pygame.freetype.Font(self.font, 20)
        self.GAME_FONT = pygame.freetype.Font(self.font, 18)
        self.SM_FONT = pygame.freetype.Font(self.font, 12)
        self.XS_FONT = pygame.freetype.Font(self.font, 8)

        try:
            g = open('poke.json')
            self.data = json.load(g)
            g.close()
        except FileNotFoundError:
            self.data = {
                "game": "crystal",
                "team": {
                    "size": 0,
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
                    "is_shiny": 0
                }
            }
            g = open('poke.json', 'w')
            g.write(json.dumps(self.data))
            g.close()

        self.game = self.data["game"]

        self.gen = 1

        if self.game == 'gold' or self.game == 'silver' or self.game == 'crystal':
            self.gen = 2

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
                "showFavorites": False,
                "favorites": [
                    "1",
                    "4",
                    "7"
                ],
                "showAttempts": False,
                "attempts": 0,
                "rbColor": True,
                "randomMail": False
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

        f = open('json/natDexToGen1Map.json')
        self.natDexToGen1Map = json.load(f)
        f.close()

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

        self.screen = pygame.display.set_mode(
            (750, 550))
        pygame.display.set_caption("Ironmon Tracker")

        self.poke_sprites = PokeSprites(self)

        self.frame_count = 0

        f = open('json/pokedex.json')
        self.pokedex = json.load(f)
        f.close()

        f = open('json/moveList1.json')
        self.move_list = json.load(f)
        f.close()

        f = open('json/items.json')
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

        self.poke_1_data = self.data["team"]["poke1"]

        if self.settings["showFavorites"]:
            self.poke_sprites.update_sprite(self, 1, {"id": self.settings["favorites"][0], "is_shiny": 0})
            self.poke_sprites.update_sprite(self, 2, {"id": self.settings["favorites"][1], "is_shiny": 0})
            self.poke_sprites.update_sprite(self, 3, {"id": self.settings["favorites"][2], "is_shiny": 0})
        else:
            self.poke_sprites.blank_sprite(self, 1)
            self.poke_sprites.blank_sprite(self, 2)
            self.poke_sprites.blank_sprite(self, 3)

    def run_game(self):
        self._update_data()
        self._update_screen()
        """Start the main loop for the game."""
        while True:
            self.frame_count += 1
            self._check_events()
            if self.frame_count > 60:
                self.frame_count = 0
                if self.settings['randomMail']:
                    if not self.mail_set and self.team_size > 0:
                        self.compose_mail()
                    self.handle_mail()
                f = open('poke.json')
                try:
                    new_data = json.load(f)
                    if self.data != new_data:
                        self.data = new_data
                        self._update_data()
                        self._update_screen()
                except JSONDecodeError:
                    continue

    def _check_events(self):
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_KP_PLUS:
                    self.modify_attempts()
                elif event.key == pygame.K_KP_MINUS:
                    self.modify_attempts(False)
                elif pressed_keys[K_RCTRL] or pressed_keys[K_LCTRL]:
                    if pressed_keys[K_KP0] or pressed_keys[K_r]:
                        self.modify_attempts()
                        self.__init__()
                    elif pressed_keys[K_s]:
                        self.update_mail_operation('2')
                    elif pressed_keys[K_m]:
                        self.compose_mail()

    def save_settings(self):
        with open("settings.json", "w") as jsonFile:
            json.dump(self.settings, jsonFile, indent=2)
        self._update_screen()

    def modify_attempts(self, add=True):
        if self.settings['showAttempts']:
            if add:
                self.settings['attempts'] += 1
            else:
                self.settings['attempts'] -= 1
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
        bg_color = pygame.Color(248, 248, 248)
        self.screen.fill(bg_color)

        for sprite in self.poke_sprites.sprites:
            sprite.blitme()

        main_x = 220

        if self.team_size > 0:
            # Name
            text_surface, rect = self.XL_FONT.render(self.decode_poke_name(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 28 + (81 * 0)))

            # Type
            text_surface, rect = self.GAME_FONT.render(self.get_type(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 60 + (81 * 0)))

            # Level
            text_surface, rect = self.GAME_FONT.render(self.get_level(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 80 + (81 * 0)))

            # Evolves
            evo = self.pokedex[self.poke_1_data['id']]['evolves_at']
            text_surface, rect = self.GAME_FONT.render('Evo: ' + evo, (0, 0, 0))
            self.screen.blit(text_surface, (main_x + 100, 80 + (81 * 0)))

            # HP
            text_surface, rect = self.GAME_FONT.render(self.get_hp(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 100 + (81 * 0)))

            # Learned Moves
            text_surface, rect = self.GAME_FONT.render(self.get_learned_moves(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 120 + (81 * 0)))

            # Next Move
            text_surface, rect = self.GAME_FONT.render(self.get_next_move(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (main_x, 142 + (81 * 0)))

            # Held Item
            if self.gen == 2:
                item = self.items[self.poke_1_data['item']]['name'].upper()
                text_surface, rect = self.GAME_FONT.render('Item: ' + item, (0, 0, 0))
                self.screen.blit(text_surface, (main_x, 165 + (81 * 0)))

        # Stats
        stat_x = 530
        stat_num_offset = 100
        stat_base_y = 0
        stat_y_offset = 28

        text_surface, rect = self.GAME_FONT.render("Atk:", (0, 0, 0))
        self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 1) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'attack'), (0, 0, 0))
        self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 1) + (81 * 0)))

        text_surface, rect = self.GAME_FONT.render("Def:", (0, 0, 0))
        self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 2) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'defense'), (0, 0, 0))
        self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 2) + (81 * 0)))

        if self.gen == 2:
            text_surface, rect = self.GAME_FONT.render("SpAtk:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 3) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'special_attack'), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 3) + (81 * 0)))

            text_surface, rect = self.GAME_FONT.render("SpDef:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 4) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'special_defense'), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 4) + (81 * 0)))

            text_surface, rect = self.GAME_FONT.render("Spd:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 5) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'speed'), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 5) + (81 * 0)))

            text_surface, rect = self.GAME_FONT.render("BST:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 6) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_bst(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 6) + (81 * 0)))
        else:
            text_surface, rect = self.GAME_FONT.render("Spd:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 3) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'speed'), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 3) + (81 * 0)))

            text_surface, rect = self.GAME_FONT.render("Spcl:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 4) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_stat(self.poke_1_data, 'special_attack'), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 4) + (81 * 0)))

            text_surface, rect = self.GAME_FONT.render("BST:", (0, 0, 0))
            self.screen.blit(text_surface, (stat_x, stat_base_y + (stat_y_offset * 5) + (81 * 0)))
            text_surface, rect = self.GAME_FONT.render(self.get_bst(self.poke_1_data), (0, 0, 0))
            self.screen.blit(text_surface, (stat_x + stat_num_offset, stat_base_y + (stat_y_offset * 5) + (81 * 0)))

        # Moves
        move_y = 220
        move_x = 20
        type_x = 290
        pp_x = 440
        pow_x = 540
        acc_x = 660

        move_y_offset = 50

        text_surface, rect = self.XL_FONT.render('Move', (0, 0, 0))
        self.screen.blit(text_surface, (move_x, move_y + (81 * 0)))

        text_surface, rect = self.XL_FONT.render('Type', (0, 0, 0))
        self.screen.blit(text_surface, (type_x, move_y + (81 * 0)))

        text_surface, rect = self.XL_FONT.render('PP', (0, 0, 0))
        self.screen.blit(text_surface, (pp_x, move_y + (81 * 0)))

        text_surface, rect = self.XL_FONT.render('Pow', (0, 0, 0))
        self.screen.blit(text_surface, (pow_x, move_y + (81 * 0)))

        text_surface, rect = self.XL_FONT.render('Acc', (0, 0, 0))
        self.screen.blit(text_surface, (acc_x, move_y + (81 * 0)))

        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_1'])['name'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, move_y + (move_y_offset * 1) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_move(self.poke_1_data['move_1'])['type'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (type_x, move_y + (move_y_offset * 1) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.poke_1_data['pp_1'], (0, 0, 0))
        self.screen.blit(text_surface, (pp_x, move_y + (move_y_offset * 1) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_1'])['power'], (0, 0, 0))
        self.screen.blit(text_surface, (pow_x, move_y + (move_y_offset * 1) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_1'])['acc'], (0, 0, 0))
        self.screen.blit(text_surface, (acc_x, move_y + (move_y_offset * 1) + (81 * 0)))

        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_2'])['name'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, move_y + (move_y_offset * 2) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_move(self.poke_1_data['move_2'])['type'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (type_x, move_y + (move_y_offset * 2) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.poke_1_data['pp_2'], (0, 0, 0))
        self.screen.blit(text_surface, (pp_x, move_y + (move_y_offset * 2) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_2'])['power'], (0, 0, 0))
        self.screen.blit(text_surface, (pow_x, move_y + (move_y_offset * 2) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_2'])['acc'], (0, 0, 0))
        self.screen.blit(text_surface, (acc_x, move_y + (move_y_offset * 2) + (81 * 0)))

        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_3'])['name'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, move_y + (move_y_offset * 3) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_move(self.poke_1_data['move_3'])['type'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (type_x, move_y + (move_y_offset * 3) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.poke_1_data['pp_3'], (0, 0, 0))
        self.screen.blit(text_surface, (pp_x, move_y + (move_y_offset * 3) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_3'])['power'], (0, 0, 0))
        self.screen.blit(text_surface, (pow_x, move_y + (move_y_offset * 3) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_3'])['acc'], (0, 0, 0))
        self.screen.blit(text_surface, (acc_x, move_y + (move_y_offset * 3) + (81 * 0)))

        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_4'])['name'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, move_y + (move_y_offset * 4) + (81 * 0)))
        text_surface, rect = self.GAME_FONT.render(self.get_move(self.poke_1_data['move_4'])['type'].upper(), (0, 0, 0))
        self.screen.blit(text_surface, (type_x, move_y + (move_y_offset * 4) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.poke_1_data['pp_4'], (0, 0, 0))
        self.screen.blit(text_surface, (pp_x, move_y + (move_y_offset * 4) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_4'])['power'], (0, 0, 0))
        self.screen.blit(text_surface, (pow_x, move_y + (move_y_offset * 4) + (81 * 0)))
        text_surface, rect = self.LG_FONT.render(self.get_move(self.poke_1_data['move_4'])['acc'], (0, 0, 0))
        self.screen.blit(text_surface, (acc_x, move_y + (move_y_offset * 4) + (81 * 0)))

        # Attempts
        attempts_y = 414
        fav_x_offset = 350  # about tree fiddy

        if self.settings["showAttempts"]:
            text_surface, rect = self.MD_FONT.render(self.get_attempts(), (0, 0, 0))
            self.screen.blit(text_surface, (move_x, attempts_y + (move_y_offset * 1) + (81 * 0)))

        if self.settings["showFavorites"]:
            text_surface, rect = self.MD_FONT.render("Favorites: ", (0, 0, 0))
            self.screen.blit(text_surface, (move_x + fav_x_offset, attempts_y + (move_y_offset * 1) + (81 * 0)))

        # Enemy Poke

        enemy_y = 450

        text_surface, rect = self.MD_FONT.render(self.get_enemy(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, enemy_y + (move_y_offset * 1) + (81 * 0)))

        text_surface, rect = self.MD_FONT.render(self.get_wild(), (0, 0, 0))
        self.screen.blit(text_surface, (move_x, enemy_y + 20 + (move_y_offset * 1) + (81 * 0)))

        pygame.display.flip()

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
        return str(self.pokedex[poke_data['id']]['type']).upper()

    def get_stat(self, poke_data, key):
        return str(poke_data[key])

    def get_learned_moves(self, poke_data):
        count_learned = 0
        total_moves = 0
        level = poke_data['level']
        moves = self.pokedex[poke_data['id']]['learns_at']
        for move in moves:
            total_moves += 1
            if move <= level:
                count_learned += 1
        return 'Learned: ' + str(count_learned) + '/' + str(total_moves)

    def get_next_move(self, poke_data):
        level = poke_data['level']
        moves = self.pokedex[poke_data['id']]['learns_at']
        for move in moves:
            if move > level:
                return 'Next at: ' + str(move)
        return 'No More Moves'

    def get_move(self, move_id):
        return self.move_list[move_id]

    def get_enemy(self):
        try:
            name = self.pokedex[self.enemy['id']]['name'].upper()
            type = self.pokedex[self.enemy['id']]['type'].upper()
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

        if self.gen == 2:
            self.has_starter = self.data["team"]["has_starter"]
            if self.has_starter > 0:
                self.mail_set = False

        self.enemy = self.data["enemy"]

        self.battle_type = self.data["battleType"]

        if "view" in self.data["team"]:
            self.view = self.data["team"]["view"]

        self.poke_1_data = self.data["team"]["poke1"]

        if self.team_size > 0:
            self.poke_sprites.update_sprite(poke, 0, self.poke_1_data, True)
        else:
            self.poke_sprites.blank_sprite(poke, 0)


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


class PokeSprites:
    """Represents a set of pokemon sprites.
    Each piece is an object of the Piece class.
    """

    def __init__(self, poke):
        """Initialize attributes to represent the overall set of pieces."""

        self.poke = poke
        self.sprites = []
        color_key = 'red'
        sheet_file = 'sprites/pokemon-rb.png'
        shiny_file = 'sprites/pokemon-rb.png'
        if poke.gen == 2:
            color_key = 'white'
            if poke.game == 'gold':
                shiny_file = 'sprites/gold-shiny.png'
                sheet_file = 'sprites/gold.png'
            elif poke.game == 'silver':
                shiny_file = 'sprites/silver-shiny.png'
                sheet_file = 'sprites/silver.png'
            else:
                shiny_file = 'sprites/crystal-shiny.png'
                sheet_file = 'sprites/crystal.png'
        elif poke.game == 'yellow':
            color_key = 'white'
            shiny_file = 'sprites/yellow.png'
            sheet_file = 'sprites/yellow.png'
        elif poke.show_color:
            color_key = 'white'
            shiny_file = 'sprites/rb-color.png'
            sheet_file = 'sprites/rb-color.png'

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

    def update_sprite(self, poke, index, poke_data, big=False):
        x = 11
        x_mult = 57
        y_mult = 57
        x_off = 1
        y_off = 1
        y = 12
        is_shiny = False

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
                if poke.gen == 2 or poke.game == 'yellow' or poke.show_color:
                    x = 11
                    y = 9
                else:
                    x = 11
                    y = 12
        rect = (x * x_mult + x_off, y * y_mult + y_off, 56, 56)
        if is_shiny:
            image = self.poke_ss_shiny.image_at(rect, self.color_key)
        else:
            image = self.poke_ss.image_at(rect, self.color_key)
        image = pygame.transform.flip(image, True, False)
        if big:
            image = pygame.transform.scale(image, (180, 180))
        poke.poke_sprites.sprites[index].image = image

    def blank_sprite(self, poke, index):
        x = 11
        x_mult = 57
        y_mult = 57
        x_off = 1
        y_off = 1
        y = 12

        if poke.gen == 2:
            x_off = 0
            y_off = 0
            x_mult = 56
            y_mult = 56
        elif poke.game == 'yellow' or poke.show_color:
            x_off = 0
            y_off = 0
            x_mult = 56
            y_mult = 56
            x = 7
            y = 9
        rect = (x * x_mult + x_off, y * y_mult + y_off, 56, 56)
        image = self.poke_ss.image_at(rect, self.color_key)
        poke.poke_sprites.sprites[index].image = image


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


if __name__ == '__main__':
    poke = Poke()
    poke.run_game()
