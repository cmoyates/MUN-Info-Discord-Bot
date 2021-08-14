import discord
from discord.ext import commands
import scrapers.calendar as calendar
import json

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(aliases=["course"])
async def getCourseDetails(ctx, *, statement):
    name = calendar.getNameFromID(statement)
    await ctx.send(name)

f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])