from requests_html import HTMLSession
import rolimons
import requests

class User:
  def __init__(self, username=None, id=None):
    if username is None:
      self.id = id
      self.username = requests.get(f'https://users.roblox.com/v1/users/{id}').json()['name']
    else:
      self.username = username
      self.id = self.query_user(username)
    self.value, self.rap, self.inventory, self.trade_ads = self.get_metadata()

  def query_user(self, username):
    request = requests.get(f'https://users.roblox.com/v1/users/search?keyword={username}&limit=10').json()
    return request['data'][0]['id']

  def get_metadata(self, refresh=False):
    # refresh javascript using HTMLSession
    if refresh is True:
      session = HTMLSession()
      request = session.get(f'https://www.rolimons.com/player/{self.id}')
    else:
      request = requests.get(f'https://www.rolimons.com/player/{self.id}')
      
    value = rolimons.get_inverse_index(request.text, '],"rap":', ',')
    trade_ad_count = rolimons.get_index(request.text, '"trade_ad_count":', ',')
    inventory = []
    rap = 0

    raw_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']
    request = requests.get(f'https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?limit=100').json()
    for item in request['data']:
      rap += item['recentAveragePrice']
      inventory.append(rolimons.Item(item['assetId'], raw=raw_data))
      
    return value, rap, inventory, trade_ad_count
