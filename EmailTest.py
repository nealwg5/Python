import configparser
import re
from datetime import timedelta

from bs4 import BeautifulSoup
from exchangelib import DELEGATE, Account, Credentials, EWSDateTime, UTC


class EmailTest(object):

    @classmethod
    def email_scan(self, keyword):

        ##grab login info from config. It's currently reading my email. Should change to a public Phia email account
        config = configparser.ConfigParser()
        config.read('\\\\pgcfpsclrfs\\ClaimDumps\\Bottest\\Python\\config.ini')
        email_username = config.get('Section', 'email_username')
        email_password = config.get('Section', 'email_password')
        email_smtp_address = config.get('Section', 'email_smtp_address')

        keyword = keyword
        credentials = Credentials(
            username=email_username,
            password=email_password
        )

        account = Account(
            primary_smtp_address=email_smtp_address,
            credentials=credentials,
            autodiscover=True,
            access_type=DELEGATE
        )

        ##Grabing date range of this week.
        end = UTC.localize(EWSDateTime.today() + timedelta(days=1))
        lastweek = EWSDateTime.today() - timedelta(days=5)
        start = UTC.localize(lastweek)

        ##Adding the file links from the email into a dictionary.
        dict = {}
        for item in account.inbox.all().filter(
                subject='FW: Scheduled Report Available For Book of Business - Subrogation') \
                .filter(datetime_received__range=(start, end)):

            ##print(item.body)
            soup = BeautifulSoup(item.body, 'lxml')
            for link in soup.findAll('a'):
                newlink = (link.get('href'))
                filtered = soup.find_all(text=re.compile(keyword))
                if 'ReportViewer' in newlink and filtered:

                    datetime = (item.datetime_received)
                    newdict = {newlink: datetime}

                    with open("\\\\pgcfpsclrfs\\ClaimDumps\\Bottest\\Python\\PythonLog.txt", 'w') as f:
                        for key, value in newdict.items():
                            f.write('%s:%s\n' % (key, value))

                    dict.update(newdict)

        return dict
