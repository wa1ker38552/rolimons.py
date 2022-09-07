import requests

class Client:
  def __init__(self, token):
    self.client = requests.Session()
    self.token = token

  def update_wishlist(self, items):
    if not isinstance(items, list): items = [items]
    data = {'asset_ids': items}
    request = self.client.post('https://www.rolimons.com/tradesettingsapi/updatewishlist', json=data, headers={'cookie': self.token})
    return request.status_code
  
  def update_asking(self, items):
    # format
    # {item: [tags, ...]}
      
    data = {'assets': []}
    for i, item in enumerate(items):
      data['assets'].append({'id': item})
      for option in items[item]:
        data['assets'][i][option] = True
    request = self.client.post('https://www.rolimons.com/tradesettingsapi/updateaskinglist', json=data)
    return request.status_code
  
  def add_player(self, username):
    request = self.client.post(f'https://www.rolimons.com/playerapi/addplayer?playername={username}')
    return request.status_code
