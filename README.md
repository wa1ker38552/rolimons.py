# RoliPY
A Python API wrapper for Rolimons.

RoliPY is an API wrapper for Rolimons that includes several features that other wrappers for Rolimons don't include. The project is being actively maintained currently.

**Getting Started** <br/>
To get started, clone the repository using, `$ git clone https://github.com/wa1ker38552/RoliPY` in shell.

# Documentaton
The wrapper contains a class along with 2 subclasses to handle and organize data. These include Rolimons, Item, and User classes.

**Rolimons** <br/>
Functions defined:

`leaderboard()` Fetches a list of players from the Rolimons leaderboard. <br/>
Example:
```py
Rolimons.leaderboard()
```
> `[{'name': Roblox, 'rank': 1, 'value': 100000, 'rap': 100000}, ...]`

`leaks()` Fetches a list of recently leaked Roblox items. <br/>
Example:
```py
for leak in Rolimons.leaks():
  print(leak['timestamp'])
  print(leak['name'])
  print(leak['image'])
```
> ```
> 123456
> Valkrie Helm
> https://tr.rbxcdn.com/...
`new_limiteds()` Fetches a list of recent items that have become limiteds. <br/>
Example:
```py
Rolimons.new_limiteds(limit=10)
```
> `[{'name': Valkrie Helm, 'rap': 100000}, ...]` <br/>

`get_trade_ads()` Fetches a list of recent trade ads. <br/>
Example:
```py
Rolimons.get_trade_ads()
```
> `[{'user': John Doe, 'offering': [<Rolimons.Item Object>, ...], 'requesting': [<Rolimons.Item Object>]}, ...]`

Note: If a trade does not have a request for items, it will switch out the `request` key with the `tag` key. <br/>
`get_market_activity()` Fetches a list of recently sold items tracked by Rolimons <br/>
Example:
```py
for item in Rolimons.get_market_activity():
  print(item['item'])
  print(item['old_rap'])
  print(item['new_rap'])
  print(item['timestamp'])
```
> ```
> <Rolimons.Item Object>
> 1000
> 1200
> 123456

**Rolimons.User** <br/>
Parameters: <br/> <br/> 
You can search for a user by id or by name when passing it as a parameter. To search for id, use `Rolimons.User(id=12345)` and to search for name, use `Rolimons.User(username='Roblox')`

Attributes: <br/> <br/> 
`self.id` User id <br/>
`self.username` User name <br/>
`self.value` Total value <br/>
`self.rap` Total rap <br/>
`self.trade_ads` Total trade ads sent <br/>
`self.inventory` All items in users inventory in `<Rolimons.Item Object>` <br/>

Functions defined: <br/> <br/> 
`get_metadata()` Refreshes all data for the specified user. This includes, rap, value, inventory, and trade_ads <br/>
Example:
```py
user = Rolimons.User('Roblox')
user.rap

user.get_metadata()
user.rap
```
> ```
> 10000
> 10001

`query_user(username)` Searches Roblox to match username to an id <br/>
Note: This function cannot be used on the client end.

**Rolimons.Item** <br/>
Parameters: <br/> <br/> 
You can only search for item by id, `Rolimons.Item(12345)`. An additional parameter you can pass in is `raw` which is the raw marketplace table containing item values. This is so that you don't hit rate limits if you try to keep searching for items. You have to pass in the 'items' key from the itemtable not the entire table.
```py
raw_data = requests.get('https://www.rolimons.com/itemapi/itemdetails').json()['items']

items = [12345, ...]
objects = []
for item in items:
  objects.append(Rolimons.Item(item, raw=raw_data))
 ```

Attributes: <br/> <br/>
`self.id` Item id <br/>
`self.name` Item name <br/>
`self.value` Item value <br/>
`self.rap` Item rap <br/>

Functions defined: <br/> <br/> 
`sales_data()` Gets Rolimons sales data about item
Example:
```py
for sale in Rolimons.Item(12345).sales_data():
  print(sale['timestamp'])
  print(sale['price'])
  print(sale['old_rap'])
  print(sale['new_rap'])
```
> ```
> 123456
> 1000
> 900
> 950
