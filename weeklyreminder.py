import datetime
import discord

from discord.ext import commands

day = datetime.datetime.today().weekday()

if day == 0:
	print("Monday")
elif day == 1:
	print("Tuesday")
elif day == 2:
	print("Wednesday")
elif day == 3:
	print("Thursday")
elif day == 4:
	print("Friday")
elif day == 5:
	print("Saturday")
elif day == 6:
	print("Sunday")
