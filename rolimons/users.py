from requests_html import HTMLSession
import rolimons
import requests
import json

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
      if item['recentAveragePrice'] is None:
        rap += 0
      else:
        rap += item['recentAveragePrice']
      inventory.append(rolimons.Item(item['assetId'], raw=raw_data))
      
    return value, rap, inventory, trade_ad_count

  def get_thumbnail(self):
    request = requests.get(f'https://www.rolimons.com/thumbnailsapi/avatarbust?userIds={self.id}&size=150x150')
    return request.json()['thumbnails'][str(self.id)]['url']

  def get_inventory_timestamps(self):
    request = requests.get(f'https://www.rolimons.com/history/{self.id}')
    return json.loads(rolimons.get_index(request.text, 'var asset_snapshot_timestamps   = ', ';'))

  def get_inventory_history(self, timestamp=None):
    if timestamp is None:
      request = requests.get(f'https://www.rolimons.com/history/{self.id}?')
    else:
      request = requests.get(f'https://www.rolimons.com/history/{self.id}?timestamp={timestamp}')

    # manually parse
    inventory = []
    raw_inventory = json.loads(rolimons.get_index(request.text, 'var player_assets               = ', ';'))

    for key in raw_inventory:
      inventory.extend([key for i in range(len(raw_inventory[key]))])

    return inventory
