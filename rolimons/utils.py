import requests
from bs4 import BeautifulSoup


class utils:
    def __init__(self):
        self.cli = requests.Session()

    def get_itemdetails(self):
        return self.cli.get('https://api.rolimons.com/items/v1/itemdetails').json()

    def get_leaderboard(self):
        request = self.cli.get('https://www.rolimons.com/leaderboard')
        soup = BeautifulSoup(request.text, 'html.parser')
        player_meta = soup.find_all('div', attrs={'class': 'pb-2 mb-3 item_cell shadow_md_35 shift_up_md mx-0'})
        players = []
        for i, p in enumerate(player_meta):
            player_soup = BeautifulSoup(str(p), 'html.parser')
            username = player_soup.find('h6', attrs={'class': 'my-0 px-2 text-light py-1 text-truncate'}).get_text()
            value_data = [user.get_text().replace('R$ ', '') for user in player_soup.find_all('span', attrs={'class': 'text-truncate'})[1:]]
            players.append(Player([i + 1, username, value_data[0], value_data[1]]))
        return players

    def get_recent_ads(self):
        request = self.cli.get('https://api.rolimons.com/tradeads/v1/getrecentads').json()
        ads = []
        if request['success']:
            for a in request['trade_ads']:
                ads.append(Ad(a))
        return ads


class Ad:
    def __init__(self, data: list):
        self.timestamp: int = data[1]
        self.user: User = User([data[2], data[3]])
        self.offer: Offer = Offer(data[4])
        self.request: Offer = Offer(data[5])


class Offer:
    def __init__(self, data: dict):
        self.items: list[int] = data['items'] if 'items' in data else None
        self.tags: list[int] = data['tags'] if 'tags' in data else None


class User:
    def __init__(self, data: list):
        self.name: str = data[1]
        self.id: int = data[0]


class Player:
    def __str__(self):
        return self.name

    def __init__(self, data: list):
        self.rank: int = data[0]
        self.name: str = data[1]
        self.value: int = data[2]
        self.rap: int = data[3]