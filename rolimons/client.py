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
