import requests
from .item import item
from .exceptions import PlayerNotFound


class player:
    def __str__(self):
        return self.name

    def __init__(self, name: str = None, id: int = None):
        self.inventory: list[item] = []

        if name is None:
            # fetch username from id
            self.query_data(id)
        else:
            # fetch id from username
            request = requests.get(f'https://api.rolimons.com/players/v1/playersearch?searchstring={name}').json()
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
        # Only works with ipv4
        request = requests.get(f'https://api.rolimons.com/players/v1/playerinfo/{id}').json()
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
            self.rolibadges: list[Rolibadges] = [Rolibadges(request['rolibadges'], badge) for badge in request['rolibadges']]
        else:
            raise PlayerNotFound(f'Player {id} does not exist')

    def refresh(self):
        # Calling player.inventory() does the exact same thing
        request = requests.get(f'https://api.rolimons.com/players/v1/playerassets/{self.id}').json()
        if request['success']:
            self.query_data(self.id)
        else:
            raise PlayerNotFound(f'Player {id} does not exist')

    def query_inventory(self):
        table = requests.get('https://api.rolimons.com/items/v1/itemdetails').json()
        assets = []

        batch = requests.get(f'https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?limit=100&sortOrder=Asc').json()
        for i in batch['data']:
            assets.append(item(i['assetId'], itemdetails=table))

        while batch['nextPageCursor'] != None:
            batch = requests.get(f'https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?limit=100&sortOrder=Asc&cursor={batch["nextPageCursor"]}').json()
            for i in batch['data']:
                assets.append(item(i['assetId'], itemdetails=table))

        self.inventory: [item] = assets
        return assets


class Rolibadges:
    def __str__(self):
        return self.name

    def __init__(self, data: dict, key: str):
        self.name: str = key
        self.obtained: int = data[key]