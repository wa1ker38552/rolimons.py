import requests

class Client:
  def __init__(self, token):
    self.client = requests.Session()
    self.client.cookies['_RoliVerification'] = token
