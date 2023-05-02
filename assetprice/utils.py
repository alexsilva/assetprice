import urllib.parse

from assetprice import settings


class Payload:
	def __init__(self, **payload):
		self.payload = payload

	@property
	def data(self):
		return urllib.parse.urlencode(self.payload)


class Url:
	def __init__(self, url: str, payload):
		self.payload = payload
		self.url = url

	def __str__(self):
		return f"{self.url}?{self.payload.data}"


class SearchPayLoad(Payload):
	def __init__(self, ticker):
		super().__init__(**{
			'q': ticker,
			'country': '',
			'type': 0
		})


class EarningPayLoad(Payload):

	def __init__(self, ticker):
		super().__init__(**{
			'companyName': ticker,
			'ticker': ticker,
			'chartProventsType': 1
		})


class SearchUrl(Url):

	def __init__(self, ticker: str):
		super().__init__(settings.SEARCH_URL, SearchPayLoad(ticker))


class EarningUrl(Url):

	def __init__(self, ticker: str):
		super().__init__(settings.EARNING_URL, EarningPayLoad(ticker))
