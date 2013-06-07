from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTEBIN
from twitter import TwitterError
import logging
import datetime


class Pastebin_ruPaste(Paste):
    def __init__(self, id):
        self.id = id
        self.headers = None
        self.url = 'http://pastebin.ru/' + self.id + '/d/'
        super(Pastebin_ruPaste, self).__init__()


class Pastebin_ru(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://pastebin.ru'
        self.sleep = SLEEP_PASTEBIN
        super(Pastebin_ru, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Pastebin.ru IDs'''
        logging.info('Retrieving Pastebin.ru ID\'s')
        #results = BeautifulSoup(helper.download(self.BASE_URL + '/archive')).find_all(
        #    lambda tag: tag.name == 'td' and tag.a and '/archive/' not in tag.a['href'] and tag.a['href'][1:])
	    url = self.BASE_URL + '/archive/' + '/'.join(str(datetime.date.today()).split('-')[0:2])
        soup = BeautifulSoup(helper.download(url))
        snip = soup.find('section','news_list')
        results = []
        for article in snip.findAll('article','item'):
	        results.append(article.header.a['href'])
        new_pastes = []
        if not self.ref_id:
            results = results[:60]
        for entry in results:
            paste = Pastebin_ruPaste(entry)
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            logging.info('Adding URL: ' + entry.url)
            self.put(entry)
    def get_paste_text(self, paste):
        return helper.download(paste.url)
