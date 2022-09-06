from discord.ext import commands
import rolimons
import discord

client = commands.Bot(command_prefix=';', help_command=None)

@client.event
async def on_ready():
  print(client.user)

@client.commands()
async def player(ctx, username):
  user = rolimons.User(username=username)
  embed = discord.Embed(title=user.username)
  embed.description = f'''
  RAP: {user.rap}
  Value: {user.value}
  Trade Ads: {user.trade_ads}
  '''

  await ctx.send(embed=embed)

@client.commands()
async def item(ctx, id):
  item = rolimons.Items(id)
  embed = discord.Embed(title=item.name)
  embed.description = f'''
  RAP: {item.rap}
  Value: {item.value}
  '''

  await ctx.send(embed=embed)

client.run('TOKEN')
