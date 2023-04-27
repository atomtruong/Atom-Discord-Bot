import discord
import json
import random
import os
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
		with open(r'/app/config/tag.json', 'r') \
				as file:
			it = json.load(file)
		if ctx.author.id != it['it']:
			await ctx.send('You are not it. <@' + str(it['it']) + '> is.')
		else:
			it['it'] = user.id
			with open(r'/app/config/tag.json', 'w') as jsonWrite:
				json.dump(it, jsonWrite, indent=4)
			await ctx.send(user.name + " is now it!")

	# Command to play Guess the Dice Roll
	@commands.command(name='guessthedice', help="Guess a number from 1-6." \
											"Ex: !guessdice 3",
					  aliases=['guessdice'])
	async def guessdice_command(self, ctx, guess: int = -1):
		if guess == -1:
			await ctx.send("You did not put a valid number.")
		elif guess > 6 or guess <= 0:
			await ctx.send("You can only guess a number from 1-6")
		else:
			answer = random.randint(1, 6)
			print(f"GuessDice Answer: {answer}")
			if guess == answer:
				await ctx.send("🎲 You guessed the right number! 🎉")
			else:
				await ctx.send("🎲 You guessed the wrong number.")

	# Command to Dice Roll
	@commands.command(name='rolldice', help="Roll a dice 1-6.",
					  aliases=['rollthedice'])
	async def rolldice_command(self, ctx: commands.Context):
		roll = random.randint(1, 6)
		print(f"RollDice: {roll}")
		await ctx.send(f"🎲 The dice has rolled... {roll}!")

	# Command for Delaney to see Linus
	@commands.command(name='linus', help='See Linus the Hamster')
	async def linus_command(self, ctx):
		linus_path = random.choice(os.listdir("/app/linus"))
		print(f"Bot sent image {linus_path}")
		await ctx.send("Here is a random photo of Linus for you :hamster:")
		await ctx.send(file=discord.File("/app/linus/"+linus_path))


def setup(bot):
	bot.add_cog(FunCog(bot))
