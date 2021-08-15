from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

urlParts = ["https://www.ratemyprofessors.com/search/teachers?query=", "&sid=U2Nob29sLTE0NDE="]

def getRMPURL(separatedProfName, firstTry):
    
    finalUrl = urlParts[0]

    loopStart = 0 if firstTry else 1
    for i in range(loopStart, len(separatedProfName)):
        finalUrl += separatedProfName[i]
        if i != len(separatedProfName)-1:
            finalUrl += "%20"

    finalUrl += urlParts[1]
    return finalUrl

def getSoupFromURL(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    return BeautifulSoup(page_html, "html.parser")

def getRatingFromProf(profName):
    profName = profName.lower()
    separatedName = profName.split(" ")
    finalUrl = getRMPURL(separatedName, True)
    print(finalUrl)

    soup = getSoupFromURL(finalUrl)

    profs = soup.find_all("a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"})

    if len(profs) == 0:
        finalUrl = getRMPURL(separatedName, False)
        print(finalUrl)
        soup = getSoupFromURL(finalUrl)
        profs = soup.find_all("a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"})
        if len(profs) == 0:
            return None

    probablyTheRightProf = None
    if len(profs) > 1:
        foundCSProf = False
        for i in range(len(profs)):
            if profs[i].find("div", {"class": "CardSchool__Department-sc-19lmz2k-0 haUIRO"}).text == "Computer Science":
                probablyTheRightProf = profs[i]
                foundCSProf = True
                break
        if not foundCSProf:
            return None
    else:
        probablyTheRightProf = profs[0]

    scoreBox = probablyTheRightProf.div.div.div.find_all("div")[1:3]
    data = scoreBox[0].text + " with " + scoreBox[1].text

    return data

'''print("Final")
print(getRatingFromProf("a vardy"))'''