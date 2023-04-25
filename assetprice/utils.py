import urllib.parse


class Payload:
	def __init__(self, **payload):
		self.payload = payload

	@property
	def data(self):
		return urllib.parse.urlencode(self.payload)


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
