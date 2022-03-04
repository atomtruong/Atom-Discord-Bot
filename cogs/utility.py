import discord
import asyncio

from discord.ext import commands


class UtilityCog(commands.Cog, name="Utility Commands", description="These "
		"commands are for utility purposes. Such as commands to help you out."):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	# Remind Me
	@commands.command(name='remindme', help='Reminds the user after x '
											'seconds/minutes/hours. NOTE: If the timer '
											'is above a minute, the timer will only '
											'update the message every minute.')
	async def remindme_command(self, ctx, timeInput):
		try:
			try:
				time = int(timeInput)
				ogtime = time
			except:
				convert_time_list = {'s':1, 'm':60, 'h':3600, 'd':86400,
									 'S':1, 'M':60, 'H':3600, 'D':86400}
				time = int(timeInput[:-1]) * convert_time_list[timeInput[-1]]
				ogtime = time
			if time > 86400:
				await ctx.send("I am unable to do timers for over a day long. "
							   "Please try again with less time.")
				return
			if time <= 0:
				await ctx.send("I am unable to do negative timers. "
							   "Please try again with more time.")
				return
			if time >= 3600:
				message = await ctx.send(f"Reminding in: {time/3600} "
										 f"hours, {time/3600//60} minutes, "
										 f"and {time%60} seconds")
			elif time >= 60:
				message = await ctx.send(f"Reminding in: {time//60}"
										 f"minutes and {time%60} seconds")
			elif time < 60:
				message = await ctx.send(f"Reminding in: "
										 f"{time} seconds")
			while True:
				try:
					if time > 60:
						await asyncio.sleep(60)
						time -= 60
					else:
						await asyncio.sleep(1)
						time -=1
					if time >= 3600:
						await message.edit(content=f"Reminding in: {time//3600} "
												   f"hours {time %3600//60} minutes {time%60} seconds")
					elif time >= 60:
						await message.edit(content=f"Reminding in: {time//60} "
												   f"minutes {time%60} seconds")
					elif time < 60:
						await message.edit(content=f"Reminding in: {time} seconds")
					if time <= 0:
						if ogtime >= 3600:
							await message.edit(content=f"Reminding "
													   f"{ctx.author.mention}. "
													   f"It has been {ogtime/3600}"
													   f"hours, {ogtime/3600//60}"
													   f" minutes, and "
													   f"{ogtime%60} seconds.")
							await ctx.send(f"{ctx.author.mention}! Your timer "
										   f"is up!")
						elif ogtime >= 60:
							await message.edit(content=f"Reminding "
													   f"{ctx.author.mention}. "
													   f"It has been "
													   f"{ogtime/3600//60} "
													   f"minutes, and "
													   f"{ogtime%60} seconds.")
							await ctx.send(f"{ctx.author.mention}! Your timer "
										   f"is up!")
						elif ogtime < 60:
							await message.edit(content=f"Reminding "
													   f"{ctx.author.mention}. "
													   f"It has been "
													   f"{ogtime%60} seconds.")
						await ctx.send(message.content)
						await message.delete()

						break
				except:
					break
		except:
			await ctx.send(f"You need to specify a time. Ex: !remindme 5s")

def setup(bot: commands.Bot):
	bot.add_cog(UtilityCog(bot))
