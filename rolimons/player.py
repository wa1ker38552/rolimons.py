import requests
from .exceptions import PlayerNotFound


class player:
    def __str__(self):
        return self.name

    def __init__(self, name: str = None, id: int = None):
        if name is None:
            # fetch username from id
            self.query_data(id)
        else:
            # fetch id from username
            request = requests.get(f'https://www.rolimons.com/api/playersearch?searchstring={name}').json()
            if request['players']:
                found = False
                for player in request['players']:
                    if name == player[1]:
                        self.id: int = request['players'][0][0]
                        self.name = request['players']
                        found = True
                        break
                if not found:
                    raise PlayerNotFound(f'Player {name} does not exist')
                else:
                    self.query_data(self.id)
            else:
                raise PlayerNotFound(f'Player {name} does not exist')

    def query_data(self, id):
        request = requests.get(f'https://www.rolimons.com/playerapi/player/{id}').json()
        if request['success']:
            self.id: int = id
            self.name: str = request['name']
            self.value: int = request['value']
            self.rap: int = request['rap']
            self.rank: int = request['rank']
            self.premium: bool = request['premium']
            self.privacy_enabled: bool = request['privacy_enabled']
            self.terminated: bool = request['terminated']
            self.stats_updated: int = request['stats_updated']
            self.last_scan: int = request['last_scan']
            self.last_online: int = request['last_online']
            self.last_location: str = request['last_location']
            self.rolibadges: list[rolibadges] = [rolibadges(request['rolibadges'], badge) for badge in request['rolibadges']]
        else:
            raise PlayerNotFound(f'Player {id} does not exist')

    def refresh(self):
        request = requests.get(f'https://www.rolimons.com/api/playerassets/{self.id}').json()
        if request['success']:
            self.query_data(self.id)
        else:
            raise PlayerNotFound(f'Player {id} does not exist')


class rolibadges:
    def __str__(self):
        return self.name

    def __init__(self, data: dict, key: str):
        self.name: str = key
        self.obtained: int = data[key]
