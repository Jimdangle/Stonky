
import os
import discord
import yfinance as yf

from dotenv import load_dotenv
from discord.ext import commands



print('\n StonkBoy 0.1 \n')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()


def stonkInfo(ticker):
	name = ticker.info['longName']
	sector = "sector: "+ticker.info['sector']
	market_cap = "market cap: $"+ str(ticker.info['marketCap'])
	opener = "open: " + str(ticker.info['open'])
	day_low = "day low: "+ str(ticker.info['dayLow'])
	day_high = "day high: " + str(ticker.info['dayHigh'])

	out_str = "STOCK: " + name +"\n"+sector+"\n"+market_cap+"\n"+opener+"\n"+day_low+"\n"+day_high

	return out_str 



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

		temp = message.content
		t_list = temp.split(' ')


		stonk = yf.Ticker(t_list[1])


		await message.channel.send(stonkInfo(stonk))

	





client.run(TOKEN)