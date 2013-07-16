'''
helper.py - provides misc. helper functions
Author: Jordan

'''

import requests
import settings
import os
import os.path
from time import sleep, strftime
import logging
import bitlyapi


r = requests.Session()


def download(url, headers=None):
    response = None
    if not headers:
        headers = None
    if headers:
        r.headers.update(headers)
	tries = 0
	while True:
        try:
            response = r.get(url).text
        except requests.ConnectionError:
            tries += 1
            logging.warn('[!] Critical Error - Cannot connect to site')
            sleep(2)
            logging.warn('[!] Retrying...')
            #response = download(url)
            if tries <= 5:
                continue
        break
    return response

def rotate():
	if os.path.exists(settings.log_file):
		os.rename(settings.log_file,settings.log_file + '.old')

def log(text):
    '''
    log(text): Logs message to both STDOUT and to .output_log file

    '''
    print(text)
    with open(settings.log_file, 'a') as logfile:
        logfile.write(text + '\n')


def build_tweet(paste):
    '''
    build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

    '''
    tweet = None
    mailhash = 0
    ret = paste.match()
    if ret != 'not_int' and ret is not None:
	if settings.USE_BITLY:
	    tweet = shortener(paste.url)
	else:
            tweet = paste.url
        if paste.type == 'db_dump':
            if paste.num_emails > 0:
                tweet += ' Emails: ' + str(paste.num_emails)
            if paste.num_hashes or paste.num_sha > 0:
                tweet += ' Hashes: ' + str(paste.num_hashes + paste.num_sha)
            if paste.num_hashes > 0 and paste.num_emails > 0:
                mailhash = str(round(paste.num_emails / float(paste.num_hashes + paste.num_sha), 2))
                tweet += ' E/H: ' + mailhash
            if paste.num_twitter > 0:
                tweet += ' TA: ' + str(paste.num_twitter)
            if paste.num_userpass > 0:
				tweet += ' U/P: ' + str(paste.num_userpass)
            #if float(mailhash) >= 0.30 and float(mailhash) <= 3: #or num_userpass > settings.EMAIL_THRESHOLD:
            #    mailarr = []
            #    for mail in paste.emails:
            #        mailarr.append(mail.split('@')[1].split('.')[0])
            #    #mailarr = sorted(set(mailarr))
            #    involved = []
            #    for i in range(0,3):
            #        try:
            #            first = max(set(mailarr),key=mailarr.count)
            #        except:
            #            break
            #        involved.append(first)
            #        while(True):
            #            try:
            #                mailarr.remove(first)
            #            except:
            #                break
            #    if len(involved) > 1:
            #        tweet += ' @' + ' @'.join(involved)

            tweet += ' Keywords: ' + str(paste.db_keywords)
        elif paste.type == 'google_api':
            tweet += ' Found possible Google API key(s)'
        elif paste.type in ['cisco', 'juniper']:
            tweet += ' Possible ' + paste.type + ' configuration'
        elif paste.type == 'ssh_private':
            tweet += ' Possible SSH private key'
        elif paste.type == 'honeypot':
            tweet += ' Dionaea Honeypot Log'
        elif paste.type == 'imei_leak':
            tweet += ' Found ' + str(paste.num_imei) + ' possible IMEIs'
	#elif paste.type == 'phone_leak':
	#    tweet += ' Found ' + str(paste.num_phonenum) + ' possibile phone numbers'
        #tweet += ' #infoleak'
    if paste.num_emails > 0:
        print(paste.emails)
    return tweet#,paste.type

def shortener(url):
	bit = bitlyapi.BitLy(settings.BITLY_USER, settings.BITLY_KEY)
	return bit.shorten(longUrl = url)['url']	
