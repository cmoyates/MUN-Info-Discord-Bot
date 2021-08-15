import discord
import json
from discord.ext import commands
from scrapers.calendar.calendar import getNameAndInfoFromID
from scrapers.banner.banner import getProfsFromCourse
from scrapers.rmp.rateMyProf import getRatingFromProfName
from scrapers.people.people import getProfInfoFromName

bot = commands.Bot(command_prefix="!")
colors = [discord.Color.blue(), discord.Color.red(), discord.Color.green(), 0]


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(aliases=["course", "courses"])
async def getCourseDetails(ctx, *, courseID):
    # Get the course name and info from the calendar
    courseName, courseInfo = getNameAndInfoFromID(courseID)
    # If there is no name, tell the user that the course doesn't exist
    if not courseName:
        await ctx.send("That course doesn't exist!")
        return
    
    # Get the profs that are teaching the course this semester and the campuses where it's being taught
    instructorData = getProfsFromCourse(courseID)
    campuses = list(instructorData.keys())

    # Get the year/level of the course
    courseYear = int(courseID[0])

    # Set up the initial embed for the message
    embed = discord.Embed(
        title=("COMP " + courseID + ": " + courseName),
        description=courseInfo,
        color=colors[courseYear-1]
    )

    # If nobody is teaching the course this semester tell the user
    if not campuses:
        embed.description += "\n\n**Nobody** is teaching this course this semester"
        await ctx.send(embed=embed)
        return

    # If this is a course without an insturctor, send the embed as is
    if not instructorData[campuses[0]]:
        await ctx.send(embed=embed)
        return

    embed.description += "\n\nProfessor(s) teaching this course this semester:\n"

    # For each campus
    for i in range(len(campuses)):
        profStrings = []
        # For each prof
        for j in range(len(instructorData[campuses[i]])):
            profString = ""
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
                profString += "**" + profName + "** (Not a listed MUN Prof) "
            # If we found the profs info in the first place
            else:
                # Get the correct name and then get try to find the RMP profile using it
                profName = profInfo["fname"] + " " + profInfo["lname"]
                rmpString, rmpName = getRatingFromProfName(profName)
                profString = profInfo["title"] + " **" + profName + "** "
            # Let the user know if a profile cannot be found, otherwise add the score to the profString
            profString += (
                " - No profile on Rate My Prof\n"
                if rmpString == None
                else " - Rate My Prof Score: " + rmpString + "\n"
            )
            profStrings.append(profString)
        # Add a field containing the campus name and all of the profStrings
        embed.add_field(
            name="__"+campuses[i]+"__",
            value="\n".join(profStrings),
            inline=False
        )

    # Send the message
    await ctx.send(embed=embed)


f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])
