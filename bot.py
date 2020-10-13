
import os
import discord
import yfinance as yf

from datetime import date 
from dotenv import load_dotenv
from discord.ext import commands



print('\n StonkBoy 0.1 \n')

load_dotenv()

#private important data fields 
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()


def getClose(ticker):
	ahoy = date.today()
	history = ticker.history(start=ahoy)

	close = history['Close'][0]

	return close

# function for reporting stock info from a given ticker
# @params accepts a ticker 
# @returns a string for output
# @problems Some tickers do not have the same dictionary keys 
# raises errors when used on a ticker with out certain data fields
def calcChange(val1, val2):
	out_val = ((val1 - val2) / val2) * 100
	sign = ""
	if out_val > 0:
		sign ="+"
	else:
		sign ="-"


	out_str = f"{out_val:.3f}"+"%"

	out_obj = [out_str,sign]

	return out_obj


def stonkInfo(ticker):
	name = ""
	sector = ""

	if 'longName' in ticker.info:
		name = ticker.info['longName']
	else:
		name = ticker.info['symbol']

	
	if 'sector' in ticker.info:
		sector = ticker.info['sector']
	else:
		sector = ticker.info['category']

	name = ":office: " + name
	sector = ":tools: " + sector

	prev = ticker.info['regularMarketPreviousClose']
	cur = getClose(ticker)

	item = calcChange(cur, prev)
	cur = f"{cur:.3f}"
	change = ""
	emoji = ""

	if item[1] =="+":
		emoji = ":arrow_up:"
		
	else:
		emoji = ":arrow_down:"

	change = "Growth: "+ emoji + " " + item[0]

	mcap = f"{ticker.info['marketCap']:,d}"
	
	market_cap = "MCap: :dollar: "+ mcap
	opener = "Op :alarm_clock: " + str(ticker.info['open'])
	day_low = "Lo :red_square: "+ str(ticker.info['dayLow'])
	day_high = "Hi :green_square: " + str(ticker.info['dayHigh'])
	cur_price = "Price :money_with_wings: "+ cur

	out_str = name +"    [ "+sector+" ]\n"
	out_str+= cur_price + "     " + change +"\n"
	out_str+= opener + "\n"
	out_str+= day_high +"     " + day_low +"\n"
	out_str+= market_cap

	return out_str 


#connecting to discord server
@client.event
async def on_ready():
	print(f'{client.user} is a gay fag')

	for guild in client.guilds:
		if guild.name == GUILD:
			break
	print(f'{client.user} is gay\n' f'{guild.name}(id: {guild.id}')


#chat commands
@client.event
async def on_message(message):
	#ignore self
	if message.author == client.user:
		return


	# easter egg / debug command
	if message.content.startswith('$oxi'):
		await message.channel.send(':dollar: Oxi sucks')


	#main command reports stock info
	if message.content.startswith('.stonk'):

		temp = message.content
		t_list = temp.split(' ')

		if t_list[1] == 'help':
			str = ""

		stonk = yf.Ticker(t_list[1])

		await message.channel.send(stonkInfo(stonk))


	





client.run(TOKEN)