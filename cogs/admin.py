import discord
import json


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
			print(f'Log: Admin {ctx.author} sent DM to {user} saying "'
				  f'{message}"')
			await user.send(message)

	# Command to set announcement channel
	@commands.command(name='set_announcement_channel')
	@commands.has_permissions(administrator=True)
	async def set_announcement_channel_command(self, ctx: commands.Context,
											   channel: int = -1):
		if channel == -1:
			channel = ctx.channel.id
			print(channel)
		with open(r'/app/config/config.json', 'r') \
				as file:
			announcement_channel = json.load(file)
		channel_message = self.bot.get_channel(announcement_channel[channel])
		print(ctx.guild)
		if self.bot.get_guild(announcement_channel['guild1']) == ctx.guild:
			print("Private Guild")
			announcement_channel['announcementChannel1'] = channel
		elif self.bot.get_guild(announcement_channel['guild2']) == ctx.guild:
			print("AI Annotations Guild")
			announcement_channel['announcementChannel2'] = channel

		with open(r'/app/config/config.json', 'w') as jsonWrite:
			json.dump(announcement_channel, jsonWrite, indent=4)
		await channel_message.send(f'I have changed the announcement channel to '
								   f'{self.bot.get_channel(channel).mention}')
		print(f"Changed Announcement Channel:"
			  f"{self.bot.get_channel(channel).name}"
			  f"(id: {self.bot.get_channel(channel).id})")

	# Command to set bot channel
	@commands.command(name='setchannel')
	@commands.has_permissions(administrator=True)
	async def setchannel_command(self, ctx: commands.Context, channel: int = -1):
		if channel == -1:
			channel = ctx.channel.id
		with open(r'/app/config/config.json', 'r') \
				as file:
			channel_file = json.load(file)
		channel_message = self.bot.get_channel(channel)
		if self.bot.get_guild(channel_file['guild1']) == ctx.guild:
			print("Private Guild")
			channel_file['channel1'] = channel
		elif self.bot.get_guild(channel_file['guild2']) == ctx.guild:
			print("AI Annotation Guild")
			channel_file['channel2'] = channel
		with open(r'/app/config/config.json', 'w') as jsonWrite:
			json.dump(channel_file, jsonWrite, indent=4)
		print(f"Changed Bot Channel: "
			  f"{self.bot.get_channel(channel).name}"
			  f"(id: {self.bot.get_channel(channel).id})")
		await channel_message.send(f'I have changed the bot channel to '
					   f'{self.bot.get_channel(channel).mention}')

	# Command to get the current bot channels
	@commands.command(name='showbotchannels')
	@commands.has_permissions(administrator=True)
	async def showbotchannels_command(self, ctx: commands.Context):
		with open(r'/app/config/config.json', 'r') \
				as file:
			data = json.load(file)
		cmd_channel1 = self.bot.get_channel(data['channel1'])
		cmd_channel2 = self.bot.get_channel(data['channel2'])

		await ctx.send(f"The bot currently works for channels: {cmd_channel1.mention}"
				 f" and {cmd_channel2.mention}")


def setup(bot):
	bot.add_cog(AdminCog(bot))
