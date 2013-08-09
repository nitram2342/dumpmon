# settings.py

USE_DB = True
DB_HOST = 'localhost'
DB_PORT = 27017

# Twitter Settings
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

#bit.ly settings
USE_BITLY = True
BITLY_USER = 'your bit.ly username'
BITLY_KEY = 'your bit.ly api_key'

# Thresholds
EMAIL_THRESHOLD = 20
HASH_THRESHOLD = 15
DB_KEYWORDS_THRESHOLD = .55
#IMEI_THRESHOLD = 30
#SHA_THRESHOLD = 30
#MD5_WP_THRESHOLD = 30

# Time to Sleep for each site
SLEEP_SLEXY = 60
SLEEP_PASTEBIN = 15
SLEEP_PASTIE = 30

# Other configuration
tweet_history = "tweet.history"
log_file = "output.log"
