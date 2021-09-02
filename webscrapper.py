from json import encoder
import requests
from bs4 import BeautifulSoup
import json


class Job():

    def __init__(self, title, place, salary, contract_type, contact_email):

        self.title = title
        self.place = place
        self.salary = salary
        self.contract_type = contract_type
        self.contact_email = contact_email


class PageParser():

    def readLinks(self):

        page = requests.get("https://www.hyperia.sk/kariera")
        soup = BeautifulSoup(page.content, "html.parser")
        job_elements = soup.find_all("a", class_="arrow-link")
        job_list = []
        for i in job_elements:
            job_list.append(i['href'])

        return job_list

    def jobPageParser(self, pagelink):

        URL = "https://www.hyperia.sk"+pagelink
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        h1 = soup.find("h1")
        title = h1.text
        colmd = soup.find_all("div", class_="col-md-4 icon")
        for i in colmd:
            text = i.find("p").text
            if "Miesto výkonu práce:" in text:
                place = text.replace("Miesto výkonu práce:", "")
            if "Platové ohodnotenie" in text:
                salary = text.replace("Platové ohodnotenie", "")
            if "Typ pracového pomeru" in text:
                contract_type = text.replace("Typ pracového pomeru", "")

        positionButton = soup.find("a", class_="position-button")
        contact_email = positionButton['href'].replace("mailto:", "")

        job = Job(title, place, salary, contract_type, contact_email)
        return job


class fileWriter():

    def writeToFile(self):

        parser = PageParser()
        jobLinks = parser.readLinks()

        jobList = []
        for link in jobLinks:
            jobList.append(vars(parser.jobPageParser(link)))

        f = open("text.txt", "w")
        f.write(json.dumps(jobList, ensure_ascii=False))
        f.close()


if __name__ == "__main__":

    f = fileWriter()
    f.writeToFile()
