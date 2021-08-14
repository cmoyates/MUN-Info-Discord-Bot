from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

calendar_url = "https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023"

def getNameFromID(courseID):
    uClient = uReq(calendar_url)
    page_html = uClient.read()
    uClient.close()

    soup = BeautifulSoup(page_html, "html.parser")

    course_divs = soup.find_all("div", {"class": "course"})

    courseIndex = -1

    for i in range(len(course_divs)):
        if course_divs[i].find("p", {"class": "courseNumber"}).text.strip() == courseID:
            courseIndex = i
            break
    
    if courseIndex == -1:
        return None
    
    course = course_divs[courseIndex]
    courseName = course.find("p", {"class": "courseTitle"}).text.strip()
    courseDesc = course.div.p.text.strip()
    return "**" + courseName + "**" + "\n" + courseName + " " + courseDesc
