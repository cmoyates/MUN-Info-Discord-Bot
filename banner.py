from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup

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

def getCourseFromID(courseID):
    #print("\n\n\n\n\n\n\n")
    output = []
    campuses = []
    searchHTML = actually_fetch_banner(2021, 1, 1)
    if not searchHTML:
        return "Something went wrong..."
    coursesByCampus = searchHTML.text.split("Campus: ")
    coursesByCampus.pop(0)
    for i in range(len(coursesByCampus)):
        courses = coursesByCampus[i].split("\nCOMP")
        campuses.append(courses.pop(0).split("\n", 1)[0].strip())
        #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        #print(campuses[i])
        #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        for j in range(len(courses)):
            if courses[j][1:5] == courseID:
                output.append([("COMP" + courses[j]).split("\n"), campuses[i]])
            #print("---- 0000 ---- 0000 ---- 0000 ---- 0000 ----")
            #print(courses[j])
        #print("---- 0000 ---- 0000 ---- 0000 ---- 0000 ----")
    return output


#print(getProfFromID("3200"))
#getAllCourses()

output = getCourseFromID("1001")

results = []
print("------------------------------")
for i in range(len(output)):
    print(output[i][1])
    topIndecies = []
    for j in range(len(output[i][0])):
        if len(output[i][0][j]) == 0:
            output[i][0] = output[i][0][0:j]
            break
        if output[i][0][j][38] != " ":
            topIndecies.append(j)
            print("------------------------------")
        print(output[i][0][j])
    print("------------------------------")
    #print(topIndecies)
    indexNum = len(topIndecies)
    topIndecies.append(len(output[i][0]))
    for j in range(indexNum):
        results.append({})
        results[len(results)-1]["Campus"] = output[i][1]
        hasProfAssigned = False
        for k in range(topIndecies[j], topIndecies[j+1]):
            containsTimes = (output[i][0][k][67:71] + output[i][0][k][72:76]).isdigit()
            containsProf = output[i][0][k][138:145] == "Primary"
            #print(containsTimes or containsProf)
            if containsProf:
                results[len(results)-1]["Prof"] = output[i][0][k][148:].strip()
                hasProfAssigned = True
            if not (containsTimes or containsProf):
                results[len(results)-1]["Notes"] = output[i][0][k].strip()
        if not hasProfAssigned:
            results[len(results)-1]["Prof"] = None

print()
#print(results)
for i in range(len(results)):
    print(results[i])