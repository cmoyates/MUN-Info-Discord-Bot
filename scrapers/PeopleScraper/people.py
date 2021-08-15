import requests
from bs4 import BeautifulSoup
import json

url = "https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1&department=Computer%20Science&lname=Anthony"
facultyStaff = eval(requests.get(url).text)["results"]


def getProfInfoFromName(profName):
    separatedName = profName.lower().split(" ")
    for i in range(len(facultyStaff)):
        correctProf = True
        for j in range(len(separatedName)):
            if separatedName[j] not in facultyStaff[i]["displayname"].lower():
                correctProf = False
                break
        if correctProf:
            return facultyStaff[i]
