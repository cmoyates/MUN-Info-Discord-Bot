import discord
from discord.ext import commands
from scrapers.CalendarScraper.calendar import getNameFromID
from scrapers.BannerScraper.banner import theRestOfTheAlgorithm
from scrapers.RMPScraper.rateMyProf import getRatingFromProf
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
    if name == None:
        await ctx.send("That course doesn't exist!")
        return
    msg = name + "\n"
    campuses, profData = theRestOfTheAlgorithm(courseID)
    if len(campuses) == 0:
        await ctx.send(msg + "\n**Nobody** is teaching this course this semester")
        return
    #print(campuses)
    msg += "\nProfessor(s) teaching this course this semester:\n"
    for i in range(len(campuses)):
        msg += "__" + campuses[i] + "__\n"
        rmpData = getRatingFromProf(profData[campuses[i]][0])
        #print(rmpData)
        msg += "**" + rmpData[0] + "**" + " (Rate My Prof Score: " + rmpData[1] + ")\n"
    #msg = msg[::len(msg)-1]
    print(msg)
    await ctx.send(msg)

f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])