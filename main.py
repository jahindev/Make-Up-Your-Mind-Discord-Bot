import discord
from decouple import config
import requests
import json
import random



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith(prefix):
        random.seed()
        print(message.content)
        args = message.content.strip().split(' ')
        if len(args) < 2 or len(args) > 3:
            await message.channel.send("Invalid syntax, use `eat [Location] [Number of options]` or `eat [Location]`")
            return
        params = {'location': args[1]}
        req = requests.get(url, params=params, headers=headers)
        text = json.loads(req.text)

        checkExist = text.get('businesses')
        if not checkExist:
            await message.channel.send(args[1] + " does not exist/has no places.")
            return

        if len(args) == 2:
            comeEat = "Come eat at " + text['businesses'][random.randint(0, len(text['businesses']) - 1)]['name']
            await message.channel.send(comeEat)
            return
        if int(args[2]) > len(text['businesses']):
            await message.channel.send("Invalid size, must be " + str(len(text['businesses'])) + " or less.")
            return
        comeEat = "Come eat at "
        newArray = random.sample(text['businesses'], int(args[2]))
        for e in newArray:
            comeEat += e['name'] + ", "
        comeEat = comeEat[:-2] 
        await message.channel.send(comeEat)
        return


headers = {'Authorization': 'Bearer %s' % config('YELP_TOKEN')}
url='https://api.yelp.com/v3/businesses/search'
prefix = 'eat '
client.run(config('DISCORD_TOKEN'))
