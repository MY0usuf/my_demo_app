 
from flask import Blueprint


app_cache = Blueprint("app_cache", __name__)


# Constants for minutes
ONE_MINUTE = 60  # 1 minute in seconds
TWO_MINUTES = 2 * ONE_MINUTE  # 2 minutes in seconds
THREE_MINUTES = 3 * ONE_MINUTE  # 3 minutes in seconds
FOUR_MINUTES = 4 * ONE_MINUTE  # 4 minutes in seconds
SIX_MINUTES = 6 * ONE_MINUTE  # 6 minutes in seconds
SEVEN_MINUTES = 7 * ONE_MINUTE  # 7 minutes in seconds
EIGHT_MINUTES = 8 * ONE_MINUTE  # 8 minutes in seconds
NINE_MINUTES = 9 * ONE_MINUTE  # 9 minutes in seconds
TEN_MINUTES = 10 * ONE_MINUTE  # 10 minutes in seconds
ELEVEN_MINUTES = 11 * ONE_MINUTE  # 11 minutes in seconds
TWELVE_MINUTES = 12 * ONE_MINUTE  # 12 minutes in seconds
THIRTEEN_MINUTES = 13 * ONE_MINUTE  # 13 minutes in seconds
FOURTEEN_MINUTES = 14 * ONE_MINUTE  # 14 minutes in seconds


# Constants for days
ONE_DAY = 24 * 60 * 60  # 1 day in seconds
TWO_DAYS = 2 * ONE_DAY  # 2 days in seconds
THREE_DAYS = 3 * ONE_DAY  # 3 days in seconds
FOUR_DAYS = 4 * ONE_DAY  # 4 days in seconds
FIVE_DAYS = 5 * ONE_DAY  # 5 days in seconds
SIX_DAYS = 6 * ONE_DAY  # 6 days in seconds
SEVEN_DAYS = ONE_DAY * 7 # 1 week in seconds
