from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup
import datetime

headers = {
    "User-Agent": "github.com/cmoyates/MUN-Info-Discord-Bot",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch",
    "Upgrade-Insecure-Requests": "1",
}

def actually_fetch_banner(year, term, level):
    data = {
        "p_term": f"{year}0{term}",
        "p_levl": f"0{level}*00",
        "campus": "%",
        "faculty": "Computer Science",
        "prof": "%",
        "crn": "%",
    }

    response = requests.post(
        "https://www5.mun.ca/admit/hwswsltb.P_CourseResults", headers=headers, data=data
    )

    soup = BeautifulSoup(response.text, "html.parser")

    h2 = soup.find_all("h2")
    if len(h2) >= 2 and h2[1].text == "No matches were found for your search":
        return None

    return soup

def getListingFromID(courseID):
    output = []
    campuses = []
    currentDate = datetime.datetime.now()
    isTerm2 = currentDate.month < 5
    year = (currentDate.year - 1) if (currentDate < datetime.datetime(currentDate.year, 4, 28)) else currentDate.year
    term = 2 if isTerm2 else 1
    searchHTML = actually_fetch_banner(year, term, 1)
    if not searchHTML:
        return "Something went wrong..."
    coursesByCampus = searchHTML.text.split("Campus: ")
    coursesByCampus.pop(0)
    for i in range(len(coursesByCampus)):
        courses = coursesByCampus[i].split("\nCOMP")
        campuses.append(courses.pop(0).split("\n", 1)[0].strip())
        for j in range(len(courses)):
            if courses[j][1:5] == courseID:
                output.append([("COMP" + courses[j]).split("\n"), campuses[i]])
    return output


def getProfAndCampusFromCourse(courseID):
    output = getListingFromID(courseID)
    results = {}
    campuses = []
    for i in range(len(output)):
        campusName = output[i][1]
        campuses.append(campusName)
        results[campusName] = []
        for j in range(len(output[i][0])):
            if len(output[i][0][j]) == 0:
                output[i][0] = output[i][0][0:j]
                break
            if output[i][0][j][38] != " ":
                profName = output[i][0][j][148:].strip()
                if len(profName) != 0:
                    isNew = True
                    for k in range(len(results[campusName])):
                        if results[campusName][k] == profName:
                            isNew = False
                    if isNew:
                        results[campusName].append(profName)
    return campuses, results