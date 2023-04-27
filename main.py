import asyncio

import discord
import os
import json
import datetime

from datetime import date
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
from pretty_help import PrettyHelp, DefaultMenu

load_dotenv()

with open('config\config.json', 'r') as file:
    data = json.load(file)

TOKEN = data["token"]
GUILD = os.getenv('DISCORD_GUILD')
REMINDED = [False, False, False, False]

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

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(data['welcomeChannel1'])
    await channel.send(f"Welcome to our server {member.mention}!")


# Makes sure that the command is only used in #atom channel.
@bot.event
async def on_message(message):
    with open("config/config.json", 'r') as file:
        data = json.load(file)
    if message.guild is None and not message.author.bot:
        print(f"User DM ({message.author}): {message.content}")
        if message.content.lower().startswith(data['prefix'] + 'linus'):
            await bot.process_commands(message)
    else:
        cmd_channel1 = bot.get_channel(data['channel1'])
        cmd_channel2 = bot.get_channel(data['channel2'])
        if message.content.lower().startswith(data['prefix']):
            if message.channel.id == cmd_channel1.id \
                    or message.channel.id == cmd_channel2.id:
                await message.delete()
                await bot.process_commands(message)
            else:
                if message.content.lower().startswith(data['prefix'] + 'setchannel'):
                    await message.delete()
                    await bot.process_commands(message)
                else:
                    await message.channel.send('Incorrect channel. Use in '
                                               + cmd_channel1.mention + ' or ' +
                                               cmd_channel2.mention)


async def weekly_call(channel, day, hour):
    global REMINDED
    channel = bot.get_channel(channel)
    if day == "Monday":
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"TA Meeting tomorrow at 10:00am!")
        REMINDED[0] = True
    elif day == "Monday" and hour == 16:
        await channel.send(f"Weekly Reminder: @everyon! "
                           f"TA Meeting at 10:00am!")
        REMINDED[1] = True

    elif day == "Thursday":
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"Meeting tomorrow at 9:00pm!")
        REMINDED[2] = True
    elif day == "Friday" and hour == 3:
        await channel.send(f"Weekly Reminder: @everyone! "
                           f"Meeting at 9:00pm!")
        REMINDED[3] = True


@tasks.loop(minutes=5)
async def background_task():
    global REMINDED
    day = date.today().strftime('%A')
    hour = datetime.datetime.now().hour
    print(f"Today is {day} Hour: {hour}")
    print(f"REMINDED[0] = {REMINDED[0]}")
    print(f"REMINDED[1] = {REMINDED[1]}")
    print(f"REMINDED[2] = {REMINDED[2]}")
    print(f"REMINDED[3] = {REMINDED[3]}")

    if day == 'Monday' or day == 'Friday' or day == 'Thursday':
        if not REMINDED[0] or not REMINDED[1] or not REMINDED[2] or not REMINDED[3]:
            with open(r'/app/config/config.json', 'r') \
                    as file:
                announcement_channel = json.load(file)
            if (day == 'Monday' and not REMINDED[0]) or (day == 'Monday' and
                                                         hour == 16 and not
                                                         REMINDED[1]) or \
                    (day == 'Thursday' and not REMINDED[2]) or \
                    (day == 'Friday' and hour == 3 and not REMINDED[3]):
                await weekly_call\
                    (announcement_channel['announcementChannel2'], day, hour)
                print("Weekly Reminder: Sent")
    else:
        print(f"Fail day: {day}")
        REMINDED[0] = REMINDED[1] = REMINDED[2] = REMINDED[3] = False


@bot.command(name='stopweekly')
@has_permissions(administrator=True)
async def stop_weekly_command(ctx):
    background_task.cancel()
    await ctx.send("Successfully stopped weekly reminder.")


@bot.command(name='startweekly')
@has_permissions(administrator=True)
async def start_weekly_command(ctx):
    background_task.start()
    await ctx.send("Successfully started weekly reminder.")


@bot.command(name='resetremind')
@has_permissions(administrator=True)
async def reset_remind_command(ctx):
    REMINDED[0] = REMINDED[1] = False


@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.logout()


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'cogs.{filename[:-3]}')
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(TOKEN)
