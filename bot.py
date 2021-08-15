import discord
import json
from discord.ext import commands
from scrapers.CalendarScraper.calendar import getNameAndInfoFromID
from scrapers.BannerScraper.banner import getProfsFromCourse
from scrapers.RMPScraper.rateMyProf import getRatingFromProfName
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
    # Get the name and description for the course
    courseName, courseInfo = getNameAndInfoFromID(courseID)
    # If there is no name, tell the user that the course doesn't exist
    if courseName == None:
        await ctx.send("That course doesn't exist!")
        return

    # Initialize the message with the info we have so far
    msg = "**COMP " + courseID + ": " + courseName + "**\n" + courseInfo + "\n"

    # Get the profs that are teaching the course this semester and the campuses where it's being taught
    instructorData = getProfsFromCourse(courseID)
    campuses = list(instructorData.keys())

    # If it's not being taught anywhere let the user know
    if not campuses:
        await ctx.send(msg + "\n**Nobody** is teaching this course this semester")
        return

    msg += "\nProfessor(s) teaching this course this semester:\n"
    # For each campus
    for i in range(len(campuses)):
        # Add the name of the campus to the message
        msg += "__" + campuses[i] + "__\n"
        # For each prof
        for j in range(len(instructorData[campuses[i]])):
            profName = ""
            rmpString = ""
            # Get their info using the dumb Banner name
            profInfo = getProfInfoFromName(instructorData[campuses[i]][j])
            # If we couldn't get any info
            if not profInfo:
                # Try to find an RMP profile using the dumb Banner name
                rmpString, rmpName = getRatingFromProfName(instructorData[campuses[i]][j])
                # If there is an RMP profile
                if rmpString:
                    profName = rmpName
                    # If there's no RMP profile either
                else:
                    profName = instructorData[campuses[i]][j]
                msg += "**" + profName + "** (Not a listed MUN Prof) "
            # If we found the profs info in the first place
            else:
                # Get the correct name and then get try to find the RMP profile using it
                profName = profInfo["fname"] + " " + profInfo["lname"]
                rmpString, rmpName = getRatingFromProfName(profName)
                msg += profInfo["title"] + " **" + profName + "** "
            # Let the user know if a profile cannot be found, otherwise add the score to the message
            msg += (
                "- No profile on Rate My Prof\n"
                if rmpString == None
                else "- Rate My Prof Score: " + rmpString + "\n"
            )
    # Send the message
    await ctx.send(msg)


f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])
