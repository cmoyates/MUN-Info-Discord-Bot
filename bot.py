import discord
import json
from discord.ext import commands
from scrapers.CalendarScraper.calendar import getNameAndInfoFromID
from scrapers.BannerScraper.banner import getProfAndCampusFromCourse
from scrapers.RMPScraper.rateMyProf import getRatingFromProf
from scrapers.PeopleScraper.people import getProfInfoFromName

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(aliases=["course", "courses"])
async def getCourseDetails(ctx, *, courseID):
    courseName, courseInfo = getNameAndInfoFromID(courseID)
    if courseName == None:
        await ctx.send("That course doesn't exist!")
        return
    msg = "**COMP " + courseID + ": " + courseName + "**\n" + courseInfo + "\n"

    campuses, instructorData = getProfAndCampusFromCourse(courseID)

    if len(campuses) == 0:
        await ctx.send(msg + "\n**Nobody** is teaching this course this semester")
        return

    msg += "\nProfessor(s) teaching this course this semester:\n"
    for i in range(len(campuses)):
        msg += "__" + campuses[i] + "__\n"
        for j in range(len(instructorData[campuses[i]])):
            profInfo = getProfInfoFromName(instructorData[campuses[i]][j])
            profName = ""
            if profInfo == None:
                profName = instructorData[campuses[i]][j]
                msg += "**" + profName + "** (Not a listed MUN Prof) "
            else:
                profName = profInfo["fname"] + " " + profInfo["lname"]
                msg += profInfo["title"] + " **" + profName + "** "
            rmpString = getRatingFromProf(profName)
            msg += (
                "- No profile on Rate My Prof\n"
                if rmpString == None
                else "- Rate My Prof Score: " + rmpString + "\n"
            )
    await ctx.send(msg)


f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])
