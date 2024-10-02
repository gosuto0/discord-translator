import discord
import json

config_json = json.load(open('./config.json', 'r'))

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    

client.run(config_json["token"])
