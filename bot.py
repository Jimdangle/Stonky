
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

print('ello')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')



client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} is a gay fag')

	for guild in client.guilds:
		if guild.name == GUILD:
			break
	print(f'{client.user} is gay\n' f'{guild.name}(id: {guild.id}')




@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$oxi'):
		await message.channel.send('Oxi sucks')

	if message.content.startswith('.stonk'):
		print(discord.version_info)
		await message.channel.send(message.content)





client.run(TOKEN)