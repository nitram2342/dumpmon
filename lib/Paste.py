from .regexes import regexes
import settings
import logging
import re

class Paste(object):
    def __init__(self):
        '''
        class Paste: Generic "Paste" object to contain attributes of a standard paste

        '''
        self.eh = 0
        self.emails = 0
        self.hashes = 0
        self.sha = 0
        self.num_sha = 0
        self.twitter = 0
        self.userpass = 0
        self.num_userpass = 0
        self.num_twitter = 0
        self.num_emails = 0
        self.num_hashes = 0
        self.text = None
        self.type = None
        self.sites = None
        self.creditcard = None
	self.num_creditcard = 0
        self.db_keywords = 0.0
        self.ssn = None
	self.num_ssn = 0
	self.cc_dump = 0
	self.num_cc_dump = 0

    def match(self):
        '''
        Matches the paste against a series of regular expressions to determine if the paste is 'interesting'

        Sets the following attributes:
                self.emails
                self.hashes
                self.num_emails
                self.num_hashes
                self.db_keywords
                self.type

        '''
        # Get the amount of emails
        self.emails = list(set(regexes['email'].findall(self.text)))
        self.hashes = regexes['hash32'].findall(self.text)
        self.sha = regexes['sha1'].findall(self.text)
        self.num_sha = len(self.sha)
        self.twitter = regexes['twitter'].findall(self.text)
        self.num_twitter = len(self.twitter)
        self.num_emails = len(self.emails)
        self.num_hashes = len(self.hashes)
        self.imei = regexes['imei'].findall(self.text)
        self.num_imei = len(self.imei)
        self.shadow = regexes['shadow'].findall(self.text)
        self.num_shadow = len(self.shadow)
        self.md5wp = regexes['md5_wp'].findall(self.text)
        self.num_md5wp = len(self.md5wp)
        self.shadow = regexes['shadow'].findall(self.text)
        self.num_shadow = len(self.shadow)
        self.sha1crypt = regexes['sha1crypt'].findall(self.text)
        self.num_sha1crypt = len(self.sha1crypt)
        self.md5crypt = regexes['md5crypt'].findall(self.text)
        self.num_md5crypt = len(self.md5crypt)
        self.sunmd5 = regexes['sun_md5'].findall(self.text)
        self.num_sunmd5 = len(self.sunmd5)
        self.total_hashes = self.num_sunmd5 + self.num_hashes + self.num_md5crypt + self.num_md5wp + self.num_shadow
	+ self.num_sha + self.num_sha1crypt
        self.userpass = regexes['userpass'].findall(self.text)
        self.num_userpass = len(self.userpass)
        self.phonenum = regexes['phonenum'].findall(self.text)
        self.num_phonenum = len(self.phonenum)
	self.creditcard = regexes['credit_card'].findall(self.text)
	self.num_creditcard = len(self.creditcard)
	self.ssn = regexes['ssn'].findall(self.text)
	self.num_ssn = len(self.ssn)
	self.cc_dump = regexes['cc_dump'].findall(self.text)
	self.num_cc_dump = len(self.cc_dump)
        if self.num_hashes > 0 or self.num_sha > 0 or self.num_md5wp > 0:
            self.eh = round(self.num_emails / float(self.num_hashes + self.num_sha + self.num_md5wp), 2)
        else:
            self.eh = 0
        if self.num_emails > 0:
            self.sites = list(set([re.search('@(.*)$', email).group(1).lower() for email in self.emails]))
        for regex in regexes['db_keywords']:
            if regex.search(self.text):
                logging.debug('\t[+] ' + regex.search(self.text).group(1))
                self.db_keywords += round(1/float(
                    len(regexes['db_keywords'])), 2)
        for regex in regexes['blacklist']:
            if regex.search(self.text):
                logging.debug('\t[-] ' + regex.search(self.text).group(1))
                self.db_keywords -= round(1.25 * (
                    1/float(len(regexes['db_keywords']))), 2)
        #if (self.num_emails >= settings.EMAIL_THRESHOLD) or ((self.num_emails >= settings.EMAIL_THRESHOLD/2) and ((self.num_hashes >= settings.HASH_THRESHOLD) or (self.num_sha >= settings.HASH_THRESHOLD) or (self.num_md5wp >= settings.HASH_THRESHOLD) or
        #(self.sha1crypt)) or (self.db_keywords >= settings.DB_KEYWORDS_THRESHOLD):
        if (self.num_emails >= settings.EMAIL_THRESHOLD) or ((self.num_emails >= settings.EMAIL_THRESHOLD/2) and (self.total_hashes > settings.HASH_THRESHOLD)) or (self.db_keywords >= settings.DB_KEYWORDS_THRESHOLD):
            self.type = 'db_dump'
        elif self.num_userpass >= settings.EMAIL_THRESHOLD:
	        self.type = 'db_dump'
        elif (self.num_imei >= settings.HASH_THRESHOLD):
            self.type = 'imei_leak'
        elif regexes['cisco_hash'].search(self.text) or regexes['cisco_pass'].search(self.text):
            self.type = 'cisco'
        elif regexes['honeypot'].search(self.text):
            self.type = 'honeypot'
        elif regexes['google_api'].search(self.text):
            self.type = 'google_api'
        #elif self.num_phonenum > settings.EMAIL_THRESHOLD:
	    #   self.type = 'phone_leak'
        #if regexes['juniper'].search(self.text): self.type = 'Juniper'
        elif self.num_creditcard > 5 or self.num_cc_dump > 5:
            self.type = 'db_dump'
        #elif self.num_ssn > 10:
	#    self.type = 'dox?'
	elif self.num_shadow > 0:
	    lines = self.text.split('\n')[:50]
	    ok = 0
	    for line in lines:
		if len(line.split(':')) == 9 and regexes['shadow'].search(line):
		    ok += 1
	    if ok > len(lines)/2:
		self.type = 'unix_shadow'
	    else:
		self.type = 'db_dump'
        for regex in regexes['banlist']:
            if regex.search(self.text):
                self.type = 'not_int'
                break
        return self.type
