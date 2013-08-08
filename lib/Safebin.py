from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTEBIN
from twitter import TwitterError
import logging
import datetime


class SafebinPaste(Paste):

    def __init__(self, id):
        self.id = id
        self.headers = None
        self.url = 'http://safebin.net' + self.id
        super(SafebinPaste, self).__init__()


class Safebin(Site):

    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://safebin.net'
        self.sleep = SLEEP_PASTEBIN
        super(Safebin, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Safebin IDs'''
        logging.info('Retrieving Safebin ID\'s')
        # results = BeautifulSoup(helper.download(self.BASE_URL + '/archive')).find_all(
        # lambda tag: tag.name == 'td' and tag.a and '/archive/' not in
        # tag.a['href'] and tag.a['href'][1:])
        url = self.BASE_URL + '/?archive'
        soup = BeautifulSoup(helper.download(url))
        snip = soup.find('table', {'class': 'archive'})
        results = []
        
	for tr in snip.findAll('tr'):
	    td = tr.findAll('td')
	    if len(td) > 0:
		if len(td[0]) < 1:
		    results.append(td[1].a['href'])
        
        #temp = []
        #try:
        #    for tr in snip.findAll('tr'):
        #        for td in tr.findAll('td'):
        #            try:
        #                temp.append(td.img['title'])
        #            except:
        #                try:
        #                    temp.append(td.a['href'], td.a['title'])
        #                except:
        #                    pass
        #    for item in temp:
        #        if len(item) > 1:  # and datetime.datetime.strptime(','.join(item[1].split(',')[0:2]), '%A %B %d, %Y') > datetime.datetime.today() - timedelta(days=1):
	#	    if item[0] != 'P':
	#		results.append(item[0])
        #except:
        #    pass
        logging.info('Found ' + str(len(results)) + ' links')
        new_pastes = []
        if not self.ref_id:
            results = results[:20]
        for entry in results:
            paste = SafebinPaste(entry)
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            logging.info('Adding URL: ' + entry.url)
            self.put(entry)

    def get_paste_text(self, paste):
        return helper.download(paste.url)
