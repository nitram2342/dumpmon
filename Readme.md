## Twitter-bot which monitors paste sites for interesting content

## Dependencies

        # pip install python-twitter
	# pip install beautifulsoup4
	# pip install requests
	# pip install pymongo <-- for MongoDB support (must have mongod running!) -->
	# pip install bitlyapi <-- to use Bit.ly url shortening -->

Next, edit the settings.py to include your Twitter application settings and bit.ly api credentials.

## Setting up MongoDB support
dumpmon has the ability to cache pastes using MongoDB. Simply setup an instance of mongod,
and set the following values in settings to the appropriate values:

	USE_DB = True
	DB_HOST = 'localhost'
	DB_PORT = 27017

If you do not want DB support, set USE_DB to False.

## Executing dumpmon

	python dumpmon.py
