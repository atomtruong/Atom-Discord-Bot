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
REMINDED = [True, True, True]

bot = commands.Bot(command_prefix=data['prefix'], help_command=PrettyHelp())

menu = DefaultMenu(delete_after_timeout=True)
bot.help_command = PrettyHelp(menu=menu, sort_commands=True, no_category='Other Commands')

# Prints the channel that the bot is in
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user} is connected to the following guilds:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')

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
    if message.guild is None and not message.author.bot:
        print(f"{message.author.name} User DM: {message.content}")
    else:
        with open("/app/config/config.json", 'r') as file:
            data = json.load(file)
        cmd_channel = bot.get_channel(data['channel'])
        cmd_channel2 = bot.get_channel(data['channel2'])
        if message.content.lower().startswith(data['prefix']):
            if message.channel.id == cmd_channel.id \
                    or message.channel.id == cmd_channel2.id:
                await message.delete()
                await bot.process_commands(message)
            else:
                if message.content.lower().startswith(data['prefix'] + 'setchannel'):
                    await message.delete()
                    await bot.process_commands(message)
                else:
                    await message.channel.send('Incorrect channel. Use in '
                                               + cmd_channel.mention + ' or ' +
                                               cmd_channel2.mention)


async def weekly_call(channel, day):
    global REMINDED
    channel = bot.get_channel(channel)
    if day == "Tuesday":
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"TA Meeting Tomorrow.")
        REMINDED[0] = True
    elif day == "Wednesday":
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"Meeting today! WAKE UP!")
        REMINDED[1] = True
    elif day == "Thursday":
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"Meeting tonight at 9:00pm!")
        REMINDED[2] = True


@tasks.loop(hours=5)
async def background_task():
    global REMINDED
    now = date.today().strftime('%A')

    if now == 'Tuesday' or now == 'Wednesday' or now == 'Thursday':
        if not REMINDED[0] or not REMINDED[1] or not REMINDED[2]:
            with open(r'/app/config/config.json', 'r') \
                    as file:
                announcement_channel = json.load(file)
            if now == 'Tuesday' and not REMINDED[0]:
                await weekly_call \
                    (announcement_channel['announcementChannel2'], now)
            elif now == 'Wednesday' and not REMINDED[1]:
                await weekly_call\
                    (announcement_channel['announcementChannel2'], now)
            elif now == 'Thursday' and not REMINDED[2]:
                await weekly_call \
                    (announcement_channel['announcementChannel2'], now)
            print("Weekly Reminder: Sent")
    else:
        print(f"Fail day: {now}")
        REMINDED[0] = REMINDED[1] = REMINDED[2] = False


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
