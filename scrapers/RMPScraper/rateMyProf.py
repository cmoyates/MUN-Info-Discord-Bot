from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

urlParts = ["https://www.ratemyprofessors.com/search/teachers?query=", "&sid=U2Nob29sLTE0NDE="]

def getRatingFromProf(profName):
    profName = profName.lower()
    separatedName = profName.split(" ")
    finalUrl = urlParts[0]

    for i in range(len(separatedName)):
        finalUrl += separatedName[i]
        if i != len(separatedName)-1:
            finalUrl += "%20"

    finalUrl += urlParts[1]

    uClient = uReq(finalUrl)
    page_html = uClient.read()
    uClient.close()

    soup = BeautifulSoup(page_html, "html.parser")

    profs = soup.find_all("a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"})
    probablyTheRightProf = profs[0]
    profFullName = probablyTheRightProf.div.find("div", {"class": "TeacherCard__CardInfo-syjs0d-1 fkdYMc"}).div.text
    #print(profFullName)
    scoreBox = probablyTheRightProf.div.div.div.find_all("div")[1:3]

    data = [profFullName, scoreBox[0].text + " with " + scoreBox[1].text]

    return data




#print(getRatingFromProf("M Hatcher"))