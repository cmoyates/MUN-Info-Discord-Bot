import discord
from discord.ext import commands
from scrapers.calendar import getNameFromID
from banner import getProfFromID
import json

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(aliases=["course"])
async def getCourseDetails(ctx, *, courseID):
    name = getNameFromID(courseID)
    prof = getProfFromID(courseID)
    await ctx.send(name + "\nProf: " + prof)

f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])