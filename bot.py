
import os
import discord
import yfinance as yf
import pandas as pd

from datetime import date
from dotenv import load_dotenv
from discord.ext import commands



print('\n StonkBoy 1.1 \n')

load_dotenv()

#private important data fields
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()


# There is a 93 character limit per line



#custom functions





# get methods

# getClose
# @param ticker (Yfinance ticker)
# @return closing price as float

def getClose(ticker):
	ahoy = date.today()
	history = ticker.history(start=ahoy)

	close = history['Close'][0]

	return close




# getRSI
# @param tick name ('aapl')
# @return rsi (float)

def getRSI(tick):
	try:
		url = f'http://www.stockta.com/cgi-bin/analysis.pl?symb={tick}&mode=table&table=rsi'

		df = pd.read_html(url)

		rsi = df[6][1][0]

		return rsi
	except:
		return "***RSI Unavailable***"






# handle data and representation

# checkField
# @params Yfinance ticker, main attribute, alternate attribute
# @returns info from main or selected field

def checkField(ticker, main, alternate):
	if main in ticker.info:
		return ticker.info[main]
	else:
		return ticker.info[alternate]





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

#write out info used to be hardcoded in stonkInfo
# @params ticker info args
# @returns a clean output
def writeInfo(*args):
	period = f"({args[8]})"
	out_str = args[0] +"    [ "+args[1]+" ]"+ period+ "\n"
	out_str+= args[2] + "     " + args[3] +"\n\n"
	out_str+= args[4] + "\n"
	out_str+= args[5] +"\n"
	out_str+= args[6] +"\n"
	out_str+= args[7]

	return out_str



# Stonk History (Brand new)
# @params ticker, starting date, ending date, or period
# - note that dates and periods can not be used together
# @ returns a already formated string for message



def stonkHistory(ticker,**alt):

	if len(alt) > 2:
		hist = ticker.history(start=alt['start_date'], end='end_date')
		str_date = alt['start_date']
		end_date = alt['end_date']
	else:
		hist = ticker.history(start=alt['start_date'], end=date.today())
		str_date = alt['start_date']


	ticker_name = ticker.info['symbol']

	init_open = hist['Open'][0]
	fin_close = hist['Close'][len(hist['Close'])-1]

	low_min = min(hist['Low'])
	high_max = max(hist['High'])

	change = calcChange(fin_close,init_open)

	count = 1

	out_str=''



	try:
		out_str += f':chart_with_upwards_trend: **{ticker_name}**     :bookmark: {str_date} :fast_forward: {end_date} \n\n'
	except:
		out_str += f':chart_with_upwards_trend: **{ticker_name}**     :bookmark: {str_date} :fast_forward: \n\n'
	out_str += f'**Open**:hourglass_flowing_sand: {init_open:.3f}     **Close**:hourglass: {fin_close:.3f}\n'
	out_str += f'**Hi** :green_square: {high_max:.3f}     **Lo** :red_square: {low_min:.3f}\n'
	out_str += f'**Change** {change[1]} {change[0]}'


	return out_str






# Main function

# stonkInfo
# @param ticker object
# @returns output string sent to discord

def stonkInfo(ticker):
 #ticker info that wont change by date (i think)
	name = checkField(ticker, 'longName', 'symbol')
	name = f":chart_with_upwards_trend: **{name}**"
	sector = checkField(ticker, 'sector', 'category')
	sector = f":tools: **{sector}**"


	#print(start_date)
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

	out_str = writeInfo(name,sector,cur,change,opener,hilo,mcap,rsi,'1d')

	return out_str






# DISCORDPY


#connecting to discord server
@client.event
async def on_ready():
	print(f'{client.user} is ALIVE')

	for guild in client.guilds:
		if guild.name == GUILD:
			break
	print(f'{client.user} is CONNECTED TO \n' f'{guild.name}(id: {guild.id}')


#chat commands
@client.event
async def on_message(message):
	#ignore self
	if message.author == client.user:
		return

	#Save Content as a string
	user_msg = message.content

	#split by spaces to use for command and input
	par_list = user_msg.split(" ")

	# first arg is always the command, second is always the ticker, 3 - N are optional and will be saved to a list based on postions +2 and up
	cmd = par_list[0]
	try:
		tick = par_list[1]
		margs = par_list[2:]
		print(margs)
	except:
		print('no other paramters found')
		tick =''
		margs = ['']


	# easter egg / debug command
	if cmd == "$oxi":
		strin = " "+tick if tick else " super hard"
		nums  = len('sucksBCDEFGHIJKLMNOPQRSTUVWXYZNOWIKNOWMYABCWONTYOUCOMEANDSHITWITHMEYOULITTLEFUCKINGBITCHIWILL')
		await message.channel.send(':dollar: Oxi sucksBCDEFGHIJKLMNOPQRSTUVWXYZNOWIKNOWMYABCWONTYOUCOMEANDSHITWITHMEYOULITTLEFUCKINGBITCHIWILLKILLUANDPUTUINADITCHUPABOVETHECLOUDSSOHIGHLIKEAPOOPUPINTHESKYTWINKLEWINKLELONGASSSTRINGNOWIHAVEAWEIRDASSTHING' + strin)
		await message.channel.send(f'{nums}')

	#main command reports stock info
	if cmd == '.stonk' or cmd == '.st':

		if tick == 'help':
			out_str = ":man_mage: **Genius Bar** \n **stonkboi 1.1** \n\n Use StonkBoi by typing .stonk or .st in chat followed by a stocks ticker \n *(new feature)* follow the stock ticker with a date or a date range \n"
			out_str += "if only one date is used it will generate stats from given date to todays date\n"
			out_str += '\n **examples** \n'
			out_str += '*.stonk aapl* or *.st aapl* this will return current data on aapl stock\n'
			out_str += '*.stonk amzn 2020-09-10* or *.st amzn 2020-09-10* this will return data on amzn stock from 09/10/2020 to Current Date \n'
			out_str += '*.stonk plm 2020-09-03 2020-09-30* or *.st plm 2020-09-03 2020-09-30* will return data on plm stock from 09/03/2020 to 09/30/2020'

			await message.channel.send(out_str)


		stonk = yf.Ticker(tick)

		if margs:
			if len(margs) > 1:
				print("Attempting three Parameters")
				await message.channel.send(stonkHistory(stonk, start_date = margs[0], end_date = margs[1]))
			else:
				print("Attempting Two Parameters")
				await message.channel.send(stonkHistory(stonk, start_date= margs[0]))
		else:
			print("Only Found a Single Parameter")
			await message.channel.send(stonkInfo(stonk))





client.run(TOKEN)
