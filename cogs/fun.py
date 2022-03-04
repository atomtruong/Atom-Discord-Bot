import discord
import json
from discord.ext import commands


class FunCog(commands.Cog, name="Fun Commands", description="These commands"
										" are for configuring your enjoyment"):
	def __init__(self, bot):
		self.bot = bot

	# First command to test to see if the bot is working in the server properly.
	@commands.command(name='repeat', help='Repeats user input. '
										  'Ex: !repeat my message')
	async def repeat_command(self, ctx, *args):
		await ctx.send("{}".format(" ".join(args)))

	# Command to play Tag
	@commands.command(name='tag', help='Tags a user if you are it. '
								  'Ex: !tag @Atom')
	async def tag_command(self, ctx, user: discord.User):
		with open(r'C:\Users\Adam\PycharmProjects\Atom\config\tag.json', 'r') \
				as file:
			it = json.load(file)
		if ctx.author.id != it['it']:
			await ctx.send('You are not it. <@' + str(it['it']) + '> is.')
		else:
			it['it'] = user.id
			with open(r'config\tag.json', 'w') as jsonWrite:
				json.dump(it, jsonWrite, indent=4)
			await ctx.send(user.name + " is now it!")


def setup(bot):
	bot.add_cog(FunCog(bot))
