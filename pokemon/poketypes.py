class PokeTypes:
    types = {
        'Normal': {
            'weak_to': ['Fighting'],
            'resists': [],
            'immune_to': ['Ghost'],
            'damage_type': 'Physical'
        },
        'Fighting': {
            'weak_to': ['Flying', 'Psychic'],
            'resists': ['Bug', 'Rock', 'Dark'],
            'immune_to': [],
            'damage_type': 'Physical'
        },
        'Poison': {
            'weak_to': ['Ground', 'Psychic'],
            'resists': ['Grass', 'Fighting', 'Poison', 'Bug'],
            'immune_to': [],
            'damage_type': 'Physical'
        },
        'Ground': {
            'weak_to': ['Grass', 'Ice', 'Water'],
            'resists': ['Poison', 'Rock'],
            'immune_to': ['Electric'],
            'damage_type': 'Physical'
        },
        'Flying': {
            'weak_to': ['Electric', 'Ice', 'Rock'],
            'resists': ['Grass', 'Fighting', 'Bug'],
            'immune_to': ['Ground'],
            'damage_type': 'Physical'
        },
        'Bug': {
            'weak_to': ['Fire', 'Flying', 'Rock'],
            'resists': ['Grass', 'Fighting', 'Ground'],
            'immune_to': [],
            'damage_type': 'Physical'
        },
        'Rock': {
            'weak_to': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
            'resists': ['Normal', 'Fire', 'Poison', 'Flying'],
            'immune_to': [],
            'damage_type': 'Physical'
        },
        'Ghost': {
            'weak_to': ['Ghost', 'Dark'],
            'resists': ['Poison', 'Bug'],
            'immune_to': ['Normal', 'Fighting'],
            'damage_type': 'Physical'
        },
        'Steel': {
            'weak_to': ['Fire', 'Ground', 'Fighting'],
            'resists': ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel'],
            'immune_to': ['Poison'],
            'damage_type': 'Physical'
        },
        'Fire': {
            'weak_to': ['Water', 'Rock', 'Ground'],
            'resists': ['Fire', 'Grass', 'Ice', 'Bug', 'Steel'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Water': {
            'weak_to': ['Electric', 'Grass'],
            'resists': ['Fire', 'Water', 'Ice', 'Steel'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Electric': {
            'weak_to': ['Ground'],
            'resists': ['Electric', 'Flying', 'Steel'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Grass': {
            'weak_to': ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'],
            'resists': ['Water', 'Electric', 'Grass', 'Ground'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Ice': {
            'weak_to': ['Fire', 'Fighting', 'Rock', 'Steel'],
            'resists': ['Ice'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Psychic': {
            'weak_to': ['Bug', 'Ghost', 'Dark'],
            'resists': ['Fighting', 'Psychic'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Dragon': {
            'weak_to': ['Ice', 'Dragon'],
            'resists': ['Fire', 'Water', 'Electric', 'Grass'],
            'immune_to': [],
            'damage_type': 'Special'
        },
        'Dark': {
            'weak_to': ['Fighting', 'Bug'],
            'resists': ['Ghost', 'Dark'],
            'immune_to': ['Psychic'],
            'damage_type': 'Special'
        }
    }

    def is_weak_to(self, defender_type, attacker_type):
        try:
            return attacker_type in self.types[defender_type]['weak_to']
        except KeyError:
            return False

    def is_immune_to(self, defender_type, attacker_type):
        try:
            return attacker_type in self.types[defender_type]['immune_to']
        except KeyError:
            return False

    def resists(self, defender_type, attacker_type):
        try:
            return attacker_type in self.types[defender_type]['resists']
        except KeyError:
            return False

    def get_multiplier_char(self, defender_types, attack):
        multiplier = 0
        if attack['cat'] == 'Status':
            return ''
        for def_type in defender_types:
            if self.is_immune_to(def_type, attack['type']):
                return '*'
            elif self.resists(def_type, attack['type']):
                multiplier -= 1
            elif self.is_weak_to(def_type, attack['type']):
                multiplier += 1
        if multiplier == 1:
            return 'ˆ'
        elif multiplier == 2:
            return '˄'
        elif multiplier == -1:
            return 'ˇ'
        elif multiplier == -2:
            return '˅'
        return ''
