import discord
import json
import asyncio

from datetime import date
from discord.ext import tasks, commands


class AdminCog(commands.Cog, name="Settings Commands", description="These "
																	  "commands are for configuring your settings."):
	def __init__(self, bot):
		self.bot = bot

	# Command to purge channel. Doesn't work very well due to
	# Discord restrictions.
	@commands.command(name='clear')
	@commands.has_permissions(administrator=True)
	async def clear_command(self, ctx: commands.Context):
		for i in range(1, 10):
			await ctx.channel.purge()

	# Command for Atom to DM user
	@commands.command(name='dm')
	@commands.has_permissions(administrator=True)
	async def dm_command(self, ctx: commands.Context, user: discord.Member = None, *, message = None):
		if user is None or message is None:
			return
		else:
			print(f"Log: Admin {ctx.author} sent DM to {user} saying "
				  f"{message}")
			await user.send(message)

	# Command to set announcement channel
	@commands.command(name='set_announcement_channel')
	@commands.has_permissions(administrator=True)
	async def set_announcement_channel_command(self, ctx: commands.Context, channel: discord.TextChannel):
		with open(r'/app/config/config.json', 'r') \
				as file:
			announcement_channel = json.load(file)
		announcement_channel['announcementChannel'] = channel
		with open(r'/app/config/config.json', 'w') as jsonWrite:
			json.dump(announcement_channel, jsonWrite, indent=4)
		await ctx.send(f'I have changed the announcement channel to {channel}')

	async def called_once_every_10second(self, channel: discord.TextChannel):
		await channel.send("10Second")

	@tasks.loop(seconds=10.0)
	async def background_task(self):
		now = date.today().weekday()
		print(now)
		with open(r'/app/config/config.json', 'r') \
				as file:
			announcement_channel = json.load(file)
		await self.called_once_every_10second\
			(announcement_channel['announcementChannel'])


def setup(bot):
	bot.add_cog(AdminCog(bot))
