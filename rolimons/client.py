import rolimons
import requests

class Client:
  def __init__(self, token):
    self.client = requests.Session()
    self.client.headers.update({'cookie': token})

    if self.post_trade_ad([1365767], ['adds'], 1, json=True)['code'] == 8:
      raise rolimons.VerificationError('Unable to authenticate token')

  def post_trade_ad(self, offering, request, id, json=False):
    request_ids, request_tags = [], []
    for item in request:
      try:
        request_ids.append(int(item))
      except ValueError:
        request_tags.append(item)
    data = {
      'offer_item_ids': offering,
      'player_id': id,
      'request_item_ids': request_ids,
      'request_tags': request_tags
    }
    request = self.client.post('https://www.rolimons.com/tradeapi/create', json=data)

    if json is True: return request.json()
    else: return request.status_code

  def update_wishlist(self, items):
    if not isinstance(items, list): items = [items]
    data = {'asset_ids': items}
    request = self.client.post('https://www.rolimons.com/tradesettingsapi/updatewishlist', json=data)
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
