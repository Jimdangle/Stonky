
import os
import discord
import yfinance as yf
import pandas as pd

from datetime import date 
from dotenv import load_dotenv
from discord.ext import commands



print('\n StonkBoy 0.1 \n')

load_dotenv()

#private important data fields 
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()




#custom functions

# getClose
# @param ticker (Yfinance ticker)
# @return closing price

def getClose(ticker):
	ahoy = date.today()
	history = ticker.history(start=ahoy)

	close = history['Close'][0]

	return close


# checkField
# @params Yfinance ticker, main attribute, alternate attribute
# @returns info from main or selected field  

def checkField(ticker, main, alternate):
	if main in ticker.info:
		return ticker.info[main]
	else:
		return ticker.info[alternate]


# getRSI
# @param tick name ('aapl')
# @return rsi (float)

def getRSI(tick):
	url = f'http://www.stockta.com/cgi-bin/analysis.pl?symb={tick}&mode=table&table=rsi'

	df = pd.read_html(url)

	rsi = df[6][1][0]

	return rsi


# calcChange
# @params value1, value2
# @return object wit

def calcChange(val1, val2):
	out_val = ((val1 - val2) / val2) * 100
	sign = ""
	if out_val > 0:
		sign =":arrow_up:"
	else:
		sign =":arrow_down:"


	out_str = f"{out_val:.3f}"+"%"

	out_obj = [out_str,sign]

	return out_obj


# stonkInfo
# @param ticker object
# @returns output string sent to discord

def stonkInfo(ticker):
	name = checkField(ticker, 'longName', 'symbol')
	name = f":office: **{name}**"
	sector = checkField(ticker, 'sector', 'category')
	sector = f":tools: **{sector}**"

	tinfo = ticker.info

	prev = tinfo['regularMarketPreviousClose']
	cur = getClose(ticker)
	difference = calcChange(cur,prev)

	cur = f'**Price**:money_with_wings: {cur:.3f}'
	change = "**Growth**" +difference[1] + " " + difference[0]

	mcap = f"**Mcap**:dollar: {tinfo['marketCap']:,d}"
	opener = f"**Open**:alarm_clock: {tinfo['open']}"
	hilo = f"***Hi*** :green_square: {tinfo['dayHigh']}     ***Lo*** :red_square: {tinfo['dayLow']}"
	rsi = f"**RSI** :muscle:{getRSI(tinfo['symbol'].upper())}"

	out_str = name +"    [ "+sector+" ]\n"
	out_str+= cur + "     " + change +"\n\n"
	out_str+= opener + "\n"
	out_str+= hilo +"\n"
	out_str+= mcap +"\n"
	out_str+= rsi

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