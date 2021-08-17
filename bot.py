import discord
import json
from discord.ext import commands
from calendarScraper import CalendarScraper
from bannerScraper import BannerScraper
from rmpScraper import RMPScraper
from peopleScraper import PeopleScraper

bot = commands.Bot(command_prefix="!")
colors = [discord.Color.blue(), discord.Color.red(), discord.Color.green(), 0]
calendar_scraper = CalendarScraper(604800) # 1 week cache lifetime
banner_scraper = BannerScraper(604800) # 1 week cache lifetime
rmp_scraper = RMPScraper(604800) # 1 week cache lifetime
people_scraper = PeopleScraper(604800) # 1 week cache lifetime


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(aliases=["course", "courses"])
async def getCourseDetails(ctx, *, course_ID):
    """Replies with info on a CS course when given the courses number/ID"""
    # Get the course name and info from the calendar
    (
        course_name,
        course_info,
    ) = await calendar_scraper.get_name_and_info_from_ID(course_ID)
    # If there is no name, tell the user that the course doesn't exist
    if not course_name:
        await ctx.send("That course doesn't exist!")
        return

    # Get the profs that are teaching the course this semester and the campuses where it's being taught
    instructor_data = await banner_scraper.get_profs_from_course(course_ID)
    campuses = list(instructor_data.keys())

    # Get the year/level of the course
    course_year = int(course_ID[0])

    # Set up the initial embed for the message
    embed = discord.Embed(
        title=(f"COMP {course_ID}: {course_name}"),
        color=colors[course_year - 1],
    )

    # If nobody is teaching the course this semester tell the user
    if not campuses:
        embed.description = (
            f"{course_info}\n\n**Nobody** is teaching this course this semester"
        )
        await ctx.send(embed=embed)
        return

    # If this is a course without an insturctor, send the embed with just the course description
    if not instructor_data[campuses[0]]:
        embed.description = course_info
        await ctx.send(embed=embed)
        return

    embed.description = (
        f"{course_info}\n\nProfessor(s) teaching this course this semester:\n"
    )

    # For each campus
    for i in range(len(campuses)):
        prof_strings = []
        # For each prof
        for j in range(len(instructor_data[campuses[i]])):
            prof_string = ""
            prof_name = ""
            rmp_string = ""
            # Get their info using the dumb Banner name
            prof_info = await people_scraper.get_prof_info_from_name(
                instructor_data[campuses[i]][j]
            )
            # If we couldn't get any info
            if not prof_info:
                # Try to find an RMP profile using the dumb Banner name
                (
                    rmp_string,
                    rmp_name,
                ) = await rmp_scraper.get_rating_from_prof_name(
                    instructor_data[campuses[i]][j]
                )
                # If there is an RMP profile
                if rmp_string:
                    prof_name = rmp_name
                    # If there's no RMP profile either
                else:
                    prof_name = instructor_data[campuses[i]][j]
                prof_string = f"**{prof_name}** (Not a listed MUN Prof) "
            # If we found the profs info in the first place
            else:
                # Get the correct name and then get try to find the RMP profile using it
                prof_name = f"{prof_info['fname']} {prof_info['lname']}"
                (
                    rmp_string,
                    rmp_name,
                ) = await rmp_scraper.get_rating_from_prof_name(prof_name)
                prof_string = f"{prof_info['title']} **{prof_name}** "
            # Let the user know if a profile cannot be found, otherwise add the score to the prof string
            prof_string += (
                " - No profile on Rate My Prof\n"
                if rmp_string == None
                else " - Rate My Prof Score: " + rmp_string + "\n"
            )
            prof_strings.append(prof_string)
        # Add a field containing the campus name and all of the prof strings
        embed.add_field(
            name="__" + campuses[i] + "__",
            value="\n".join(prof_strings),
            inline=False,
        )

    # Send the message
    await ctx.send(embed=embed)


f = open("config.json")
data = json.load(f)
f.close()

bot.run(data["token"])
