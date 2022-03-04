import discord
import json
import os

from discord.ext import commands


class SettingsCog(commands.Cog, name="Settings Commands", description="These "
								"commands are for configuring your settings."):
	def __init__(self, bot):
		self.bot = bot

	# Command to change prefix
	@commands.command(name='prefix', help='Change the prefix for the bot. '
										  'Only one character. Enter no input '
										  '(!prefix) to get current prefix. '
										  'Ex: !prefix ?')
	async def prefix_command(self, ctx: commands.Context, user_prefix=''):
		with open(r'C:\Users\Adam\PycharmProjects\Atom\config\config.json', 'r') \
				as file:
			data = json.load(file)
		if len(user_prefix) == 0:
			await ctx.send('This server\'s prefix is ' + data['prefix'])
		elif len(user_prefix) != 1:
			error = 'Please make sure that you are only using one character.'
			await ctx.send(error)
		else:
			data['prefix'] = user_prefix
			with open("config\config.json", "w") as jsonWrite:
				json.dump(data, jsonWrite, indent=4)
			await ctx.send(f'Prefix changed to: {user_prefix}')
			bot.command_prefix = data['prefix']


def setup(bot):
	bot.add_cog(SettingsCog(bot))
