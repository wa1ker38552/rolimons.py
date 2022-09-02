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
