import configparser
import sys

import requests
from bs4 import BeautifulSoup

from EmailTest import EmailTest


class Download(object):

    def download_file(self, URL, keyword, currentDate):
        linkURL = URL

        config = configparser.ConfigParser()
        config.read('\\\\pgcfpsclrfs\\ClaimDumps\\Bottest\\Python\\config.ini')
        Premier_UserName = config.get('Section', 'Premier_UserName')
        Premier_Password = config.get('Section', 'Premier_Password')

        username = Premier_UserName
        password = Premier_Password

        s = requests.Session()
        r = s.get(linkURL)

        realURL = r.url

        soup = BeautifulSoup(r.content, 'lxml')

        VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
        VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
        EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']

        login_data = (
            ('__VIEWSTATE', VIEWSTATE),
            ('__VIEWSTATEGENERATOR', VIEWSTATEGENERATOR),
            ('__EVENTVALIDATION', EVENTVALIDATION),
            ('txtUserID', username),
            ('PasswordBox', password),
            ('btnLogin', 'Log+In')
        )

        r = s.post(realURL, data=login_data)
        resp = s.get(r.url)

        zname = "\\\\pgcfpsclrfs\\ClaimDumps\\Premier\\Download\\" + keyword + currentDate + ".zip"
        zfile = open(zname, 'wb')
        zfile.write(resp.content)
        zfile.close()
        print(zname + 'completed')

    def email_download(self, fileName):
        emailURL = EmailTest.email_scan(fileName)
        while len(emailURL.keys()) > 0:
            i = len(emailURL.keys()) - 1
            key = list(emailURL.keys())[i]
            value = list(emailURL.values())[i]
            convertedDate = value.strftime('%Y-%m-%d')
            emailURL.popitem()
            self.download_file(key, fileName, convertedDate)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sysarg = sys.argv[1]

test = Download()
test.email_download(sysarg)
##test.email_download('IHA Weekly')
##test.email_download('Phia Eligibility')
##test.email_download('BCBS Monthly')
