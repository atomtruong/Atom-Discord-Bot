import discord
import os
import json
from datetime import date

from discord.ext import tasks, commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp, DefaultMenu

load_dotenv()

with open("/app/config/config.json", 'r') as file:
    data = json.load(file)

TOKEN = data["token"]
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix=data['prefix'], help_command=PrettyHelp())

menu = DefaultMenu(delete_after_timeout=True)
bot.help_command = PrettyHelp(menu=menu, sort_commands=True, no_category='Other Commands')

# Prints the channel that the bot is in
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
    )

    await bot.change_presence(
        activity=discord.Game(name="Python Bot Simulator")
    )

    background_task.start()

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(data['welcomeChannel'])
    await channel.send(f"Welcome to our server {member.mention}!")

# Makes sure that the command is only used in #atom channel.
@bot.event
async def on_message(message):
    cmd_channel = bot.get_channel(data['channel'])
    if message.content.lower().startswith(data['prefix']):
        if message.channel.id == cmd_channel.id:
            await message.delete()
            await bot.process_commands(message)
        else:
            await message.channel.send('Incorrect channel. Use in '
                                       + cmd_channel.mention)


async def called_once_every_10second(channel):
    channel = bot.get_channel(channel)
    await channel.send("10Second")


@tasks.loop(seconds=10.0)
async def background_task():
    now = date.today().weekday()
    print(now)
    with open(r'/app/config/config.json', 'r') \
            as file:
        announcement_channel = json.load(file)
    await called_once_every_10second \
        (announcement_channel['announcementChannel'])


@bot.command(name='stop')
async def stop_command():
    background_task.stop()


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(TOKEN)
