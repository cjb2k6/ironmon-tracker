class Default:
    def __init__(self):
        self._data = {
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
        self._settings = {
                "showFavorites": False,
                "favorites": [
                    "1",
                    "4",
                    "7"
                ],
                "showAttempts": False,
                "attempts": 0,
                "rbColor": True,
                "randomMail": False,
                "borderType": -1
            }

    def data(self):
        return self._data

    def settings(self):
        return self._settings

