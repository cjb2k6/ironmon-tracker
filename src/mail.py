import json
import os
import numpy as np


class Mail:
    def __init__(self, encode_char_map, decode_char_map):
        # Check if mail file exists, create if not
        try:
            f = open('../mail')
            f.close()
        except FileNotFoundError:
            f = open('../mail', 'w')
            f.write('0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,78,0,0'
                    ',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
            f.close()

        self.jsonPath = os.path.join(os.getcwd(), 'json', 'mail.json')

        try:
            f = open(self.jsonPath)
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
            f = open(self.jsonPath, 'w')
            f.write(json.dumps(self.mail, indent=2))
            f.close()

        self.mail_set = True
        self.mail_initialized = False
        self.encode_char_map = encode_char_map
        self.decode_char_map = decode_char_map

    def handle_mail(self):
        f = open("../mail", 'r')
        tokens = f.read().split(',')
        f.close()

        if len(tokens) > 0:
            operation = tokens[0]
            if operation == "3":
                self.save_mail(tokens)

    def update_mail_operation(self, op):
        f = open("../mail", 'r')
        tokens = f.read().split(',')
        f.close()

        tokens[0] = op
        output = ",".join(tokens)

        f = open("../mail", 'w')
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
        with open(self.jsonPath, "w") as jsonFile:
            json.dump(self.mail, jsonFile, indent=2)

        # Set mail operation back to "0"
        tokens[0] = '0'
        output = ",".join(tokens)

        f = open("../mail", 'w')
        f.write(output)
        f.close()

    def compose_mail(self, signature):
        if len(self.mail) > 0:
            mail = self.mail[np.random.randint(0, len(self.mail))]
            self.send_mail(mail, signature)

    def send_mail(self, mail, signature):
        print('Sending Mail...')
        encoded_message = '1,'
        encoded_message += self.encode_line(mail['line1'])
        encoded_message += ',78,'
        encoded_message += self.encode_line(mail['line2'])
        encoded_message += signature

        f = open("../mail", "w")
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

