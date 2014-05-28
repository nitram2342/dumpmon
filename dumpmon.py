# dumpmon.py
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Refine Regex
#	- Create/Keep track of statistics

from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.Pastie import Pastie, PastiePaste
from lib.Pastebin_ru import Pastebin_ru, Pastebin_ruPaste
from lib.Safebin import Safebin, SafebinPaste
from lib.Nopaste import Nopaste, NopastePaste
from lib.helper import log
from lib.helper import rotate
from time import sleep
from twitter import Twitter, OAuth
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, log_file, USE_TWITTER, \
    USE_PASTEBIN, USE_SLEXY, USE_PASTIE, USE_PASTEBIN_RU, USE_NOPASTE, USE_SAFEBIN

import threading
import logging


def monitor():
    '''
    monitor() - Main function... creates and starts threads

    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="more verbose", action="store_true")
    args = parser.parse_args()
    rotate()
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s', filename=log_file, level=level)
    logging.info('Monitoring...')
    if USE_TWITTER:
        bot = Twitter(
            auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                       CONSUMER_KEY, CONSUMER_SECRET))
    else:
        bot = None
    # Create lock for both output log and tweet action
    log_lock = threading.Lock()
    tweet_lock = threading.Lock()

    threads = []

    if USE_PASTEBIN:
        threads.append(threading.Thread(
                target=Pastebin().monitor, args=[bot, tweet_lock]))
    if USE_SLEXY:
        threads.append(threading.Thread(
            target=Slexy().monitor, args=[bot, tweet_lock]))
    if USE_PASTIE:
        threads.append(threading.Thread(
                target=Pastie().monitor, args=[bot, tweet_lock]))
    if USE_PASTEBIN_RU:
        threads.append(threading.Thread(
                target=Pastebin_ru().monitor, args=[bot, tweet_lock]))
    if USE_NOPASTE:
        threads.append(threading.Thread(
                target=Nopaste().monitor, args=[bot, tweet_lock]))
    if USE_SAFEBIN:
        threads.append(threading.Thread(
                target=Safebin().monitor, args=[bot, tweet_lock]))

    for thread in threads:
        thread.daemon = True
        thread.start()

    # Let threads run
    try:
        # i = 0
        while(1):
        #    i += 1
            sleep(5)
        #    if i == 6:
        #	for thread in (pastebin_thread, slexy_thread, pastie_thead, pastebin_ru_thread, nopaste_thread):
        #		if not thread.isAlive:
        #			thread.daemon = True
        #			thread.start()
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
