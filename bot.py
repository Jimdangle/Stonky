
import os
import discord
import yfinance as yf
import pandas as pd
import time

import datetime as dt
from dotenv import load_dotenv
from discord.ext import commands



print('\n StonkBoy 2.0 \n')

load_dotenv()

#private important data fields
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()


# There is a 93 character limit per line



#custom functions




# get methods


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
		return "***NA***"







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
	out_val = ((val2 - val1) / val1) * 100
	sign = ""
	if out_val > 0:
		sign =":arrow_up:"
	else:
		sign =":arrow_down:"


	out_str = f"{out_val:.3f}"
	out_fl = float(out_str)

	out_obj = [out_fl,sign]

	return out_obj


# can only compare in a single dimension of list
# takes in as many numbers as you want
# returns the maximum value, maximum values pos in the list, the minimum value, and the minimum values pos in the par_list

def compare(*args):

	max = args[len(args)-1]
	max_pos = 0
	min = args[len(args)-1]
	min_pos = 0

	if len(args) > 2:
		print('somethings to compare')
		for i in range(len(args)):
			if args[i] > max:
				max = args[i]
				max_pos = i
				#print(max)
			if args[i] < min:
				min = args[i]
				min_pos = i
				#print(min)

		return {'max':[max,max_pos],'min':[min,min_pos]}
	elif len(args) == 2:
		if args[0] > args[1]:
			return {'max':[args[0],0],'min':[args[1],1]}
		else:
			return {'max':[args[1],1],'min':[args[0],0]}
	else:
		return {'max':[args[0],0],'min':[args[0],0]}




# Updated Stonk Info for the Modern Era
# Now you can pass it any amount of arguments
# it will sort through dates, and stocks
# then it will figure out the appropriate action to represent them
# it would get passed a list of strings like 'aapl', 'amzn', '2020-10-01'
# then it will return a object of the requested Info
# then using the compare method it will figure out the overall winner of each category

def stonkInfo(*args):

	emojis = {'chart':":chart_with_upwards_trend:",'dolwing':":money_with_wings:",'alarm':":alarm_clock:",'gr':":green_square:",'r':":red_square:",'muscle':":muscle:",'win':":crown:" }


	stocks = []
	dates = []

	#this will contain the stock objects for output to another method
	stonks = {}

	# differentiates between a date and stocks
	for arg in args:
		if len(arg) > 4:
			if len(dates) < 2:
				dates.append(arg)
		else:
			stocks.append(arg.upper())

	print(dates)
	print(stocks)

	#General finance info from tickers
	tickers = []

	#I needed this to get market cap, about it really
	tinfos = []
	#im gonna move forward with this being gone


	date_length = len(dates)
	print(date_length)
	stocks_length = len(stocks)

	if date_length == 0:
		daychecker = dt.date.today().weekday()
		if daychecker == 6:
			time_diff = dt.timedelta(1)
			date = dt.date.today() - time_diff
		elif daychecker == 7:
			time_diff = dt.timedelta(2)
			date = dt.date.today() - time_diff
		else:
			date = dt.date.today()

		tickers = yf.download(stocks,start=date)
		print(tickers)
	elif date_length == 1:
		tickers = yf.download(stocks, start=dates[0], end= dt.date.today())
	elif date_length == 2:
		tickers = yf.download(stocks, start= dates[0], end = dates[1])



	print(tickers.keys())

	open = []
	close = []
	high = []
	low = []
	over_change = []

	#print(tickers['Adj Close'])
	# clacChange outputs an object (0: float of change formated to .001, 1: up or down arrow)
	# use reactions to get specific info on a stock

	over_length = len(tickers['Open']) - 1

	if date_length == 1 or date_length == 2:
		if stocks_length ==1:
			open.append(tickers['Open'][0])
			open.append(tickers['Open'][over_length])

			close.append(tickers['Close'][0])
			close.append(tickers['Close'][over_length])

			for i in range(over_length+1):
				high.append(tickers['High'][i])
				low.append(tickers['Low'][i])

				over_change.append(calcChange(open[0],close[1]))
				max_high = compare(*high)['max'][0]
				min_low = compare(*low)['min'][0]



		else:
			count =0
			for stonk in stocks:
				open.append([tickers['Open'][stonk][0],tickers['Open'][stonk][over_length]])
				close.append([tickers['Close'][stonk][0],tickers['Close'][stonk][over_length]])
				over_change.append(calcChange(open[0],close[1]))
				count += 1

				high.append([tickers['High'][stonk][0],tickers['High'][stonk][over_length]])
				low.append([tickers['Low'][stonk][0],tickers['Low'][stonk][over_length]])
	else:


		if stocks_length == 1:
			open.append(tickers['Open'][0])
			close.append(tickers['Close'][0])
			high.append(tickers['High'][0])
			low.append(tickers['Low'][0])

			over_change.append(calcChange(open[0],close[0]))

		else:
			for stonk in stocks:
				open.append(tickers['Open'][stonk][0])
				close.append(tickers['Close'][stonk][0])
				low.append(tickers['Close'][stonk][0])
				high.append(tickers['High'][stonk][0])
				over_change.append(calcChange(open[0],close[0]))

	ticker_str = ''
	open_str = ''
	close_str =''
	high_str =''
	low_str = ''
	change_str = ''
	rsi = ''
	for i in range(len(stocks)):
		ticker_str += f"{emojis['chart']}{stocks[i]:<9}"
		open_str += f"{emojis['dolwing']}{close[i]:.3f} "
		close_str += f"{emojis['alarm']}{open[i]:.3f} "
		high_str += f"{emojis['gr']}{high[i]:.3f} "
		low_str += f"{emojis['r']}{low[i]:.3f} "
		change_str += f"{over_change[i][1]}{over_change[i][0]:.3f} "
		rsi += f"{emojis['muscle']}{getRSI(stocks[i]):.2f}"

	out_str = f" {ticker_str:} {dates}\n {open_str:>11} \n {close_str:>11} \n {high_str:>11} \n {low_str:>11} \n {change_str:>11} \n {rsi:>11}"

	return out_str









def helpMenu():
	print('Help Menu')





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
	args = user_msg.split(" ")

	command = args[0]

	args = args[1:]

	if command == ".st" or command == ".stonk":
		await message.channel.send(stonkInfo(*args))

	if command == ".sth" or command == '.stonkh':
		helpMenu()









client.run(TOKEN)
