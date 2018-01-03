import json

'''
This class is for serializing and deserializing different objects for data trasfer between client and server
'''
class ObjectFactory():
    def __init__(self):
        pass

    @staticmethod
    def field_to_json(field):
        field_json = json.dumps(field)
        return field_json

    @staticmethod
    def field_from_json(field_json):
        field_arr = json.loads(field_json)
        return field_arr

    @staticmethod
    def players_to_json(players):
        players_arr = []
        for player in players.values():
            players_arr.append((player.get_username(), player.get_score()))

        players_json = json.dumps(players_arr)
        return players_json

    @staticmethod
    def players_from_json(players_json):
        players_arr = json.loads(players_json)
        return players_arr