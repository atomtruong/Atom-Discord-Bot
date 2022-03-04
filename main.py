import discord
import os
import json
from datetime import date

from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from pretty_help import PrettyHelp, DefaultMenu

load_dotenv()

with open("/app/config/config.json", 'r') as file:
    data = json.load(file)

TOKEN = data["token"]
GUILD = os.getenv('DISCORD_GUILD')
REMINDED = False

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
            if message.content.lower().startswith(data['prefix'] + 'setchannel'):
                await message.delete()
                await bot.process_commands(message)
            else:
                await message.channel.send('Incorrect channel. Use in '
                                           + cmd_channel.mention)


async def called_once_every_tuesday(channel):
    global REMINDED
    channel = bot.get_channel(channel)
    await channel.send(f"Weekly Reminder: @everyone. Meeting with TA!")
    REMINDED = True


@tasks.loop(hours=5)
async def background_task():
    global REMINDED
    now = date.today().weekday()
    if now == 1:
        if REMINDED is False:
            with open(r'/app/config/config.json', 'r') \
                    as file:
                announcement_channel = json.load(file)
            await called_once_every_tuesday \
                (announcement_channel['announcementChannel'])
            print("Weekly Reminder: Sent")
    else:
        print(f"Fail {now}")
        REMINDED = False


@bot.command(name='stopweekly')
@has_permissions(administrator=True)
async def stop_weekly_command(ctx):
    background_task.stop()
    ctx.send("Successfully stopped weekly reminder.")

@bot.command(name='startweekly')
@has_permissions(administrator=True)
async def start_weekly_command(ctx):
    background_task.start()
    ctx.send("Successfully started weekly reminder.")

@bot.command(name='resetremind')
@has_permissions(administrator=True)
async def reset_remind_command(ctx):
    global REMINDED
    REMINDED = False

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(TOKEN)
