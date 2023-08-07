from django.conf import settings
from decimal import Decimal

API_URL = settings.ENV.str("API_URL", default=None)

SEARCH_URL = API_URL + "/home/mainsearchquery"
EARNING_URL = API_URL + "/acao/companytickerprovents"

BAZIN_TAX = Decimal(6)
BAZIN_TAX = Decimal(100) / BAZIN_TAX

TICKER_VALIDATOR = getattr(settings, "TICKER_VALIDATOR", None)

SELENIUM_CHROME_EXECUTABLE_PATH = getattr(settings, "SELENIUM_CHROME_EXECUTABLE_PATH", None)

if SELENIUM_CHROME_EXECUTABLE_PATH is None:
	SELENIUM_CHROME_EXECUTABLE_PATH = "chromedriver"
