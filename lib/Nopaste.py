from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_SLEXY
from twitter import TwitterError
import logging
import datetime


class NopastePaste(Paste):

    def __init__(self, id):
        self.id = id
        self.headers = None
        self.url = 'http://nopaste.me/raw/' + self.id + '.txt'
        super(NopastePaste, self).__init__()


class Nopaste(Site):

    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://nopaste.me'
        self.sleep = SLEEP_SLEXY
        super(Nopaste, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Pastebin IDs'''
        logging.info('Retrieving Nopaste ID\'s')
        results = []
        # results = BeautifulSoup(helper.download(self.BASE_URL + '/archive')).find_all(
        # lambda tag: tag.name == 'td' and tag.a and '/archive/' not in
        # tag.a['href'] and tag.a['href'][1:])
        url = self.BASE_URL + '/recent'
        try:
            soup = BeautifulSoup(helper.download(url))
            snip = soup.find('div', {'class': 'grid_12 content'})

            for div in snip.findAll('div', {'class': 'grid_3 info'}):
                try:
                    temp = div.a['href']
                except:
                    pass
                if '#' not in temp:
                    results.append(temp.split('/')[-1])
        except:
            # print 'some error downloading/parsing Nopaste at ' + str(datetime.datetime.now())
            # outfile = open('Nopaste.error','w')
            # outfile.write(soup.prettify())
            # outfile.close()
            pass
            #logging.info('some error downloading/parsing Nopaste at ' + str(datetime.datetime.now())
        new_pastes = []
        if not self.ref_id:
            results = results[:60]
        for entry in results:
            paste = NopastePaste(entry)
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            logging.info('Adding URL: ' + entry.url)
            self.put(entry)

    def get_paste_text(self, paste):
        return helper.download(paste.url)
