import discord

from discord.ext import commands


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


def setup(bot):
	bot.add_cog(AdminCog(bot))
