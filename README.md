# MUN Info Discord Bot

This is a Discord bot that I made with the intention of turning it into a plugin for [Automata](https://github.com/MUNComputerScienceSociety/Automata). This is the repo for the standalone version, but you can see it in its plugin form [here](https://github.com/MUNComputerScienceSociety/Automata/tree/master/plugins/Course).

This bot lets the user give it the course number for any undergrad CS course and recieve some info about said course.

You can click [here](https://discord.com/api/oauth2/authorize?client_id=875977879064834049&permissions=8&scope=bot) to add the bot to any Discord server you're an admin on.

## What info does it give?
- The name of the course
- A description of the course from MUNs [calendar](https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023)
- The professors that are teaching the course in the current semester
- The [Rate My Professors](https://www.ratemyprofessors.com/) score (and number of reviews) for each of those profs

## How does it work?
It's just a bunch of web scrapers. It scrapes the aforementioned [calendar](https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023), MUNs Banner system, MUNs [directory of all of their professors](https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1), and the [Rate My Professors](https://www.ratemyprofessors.com/) website. After it scrapes a particular bit of data once it caches it for a week using a mongodb database, just to prevent any rate limiting / banning.

## Credits
This project was loosely inspired by [yaMUN](https://github.com/jackharrhy/yaMUN) which is a project done by a few of my classmates in a web development course last year.

There is also a bit of code which I copied directly from [muntrunk](https://github.com/jackharrhy/muntrunk) (specifically lines 10 - 19 and 38 - 60 of [this file](https://github.com/cmoyates/Automata/blob/master/plugins/Course/bannerScraper.py) are copied from lines 9 - 41 of [this file](https://github.com/jackharrhy/muntrunk/blob/master/muntrunk/scrape.py#L12)) so full credit to [Jack](https://github.com/jackharrhy) for those parts.

Everything else was done by me!
