import statistics
from decimal import Decimal

from assetprice import settings
from ._driver import BaseWebDriverCommand, ResponseResult
from ...utils import SearchUrl, EarningUrl


class Command(BaseWebDriverCommand):
	"""O comando calcula o preço teto com base na fórmula do Décio Bazin"""

	@classmethod
	def get_price(cls, response: ResponseResult):
		price = response.data[0]['price']
		price = price.replace(',', '.')
		price = Decimal(price)
		return price

	@classmethod
	def get_max_price(cls, response: ResponseResult):
		yearly = response.data['assetEarningsYearlyModels']
		avg = statistics.mean([item['value'] for item in yearly])
		price = Decimal(avg) * settings.BAZIN_TAX
		return price, avg

	@staticmethod
	def get_url(url, payload):
		return url + "?" + payload.data

	def get_spec(self, **options):
		"""Extra e calcula o preço teto"""
		ticker = options['ticker']

		response = self.get_json(str(SearchUrl(ticker)))
		if options['verbosity'] > 2:
			print(response)
		price = self.get_price(response)

		response = self.get_json(str(EarningUrl(ticker)))
		if options['verbosity'] > 2:
			print(response)

		max_price, avg = self.get_max_price(response)

		data = {
			'price': price,
			'max_price': max_price,
			'diff': max_price - price,
			'avg': avg
		}
		return data

	def handle(self, *args, **options):
		""""""
		ticker = options['ticker']
		print("Código: ", ticker, file=self.stdout)

		data = self.get_spec(**options)

		price = data['price']
		max_price = data['max_price']
		diff = data['diff']
		avg = data['avg']

		print(f"Taxa aplicada: {settings.BAZIN_TAX:.5}", file=self.stdout)
		print(f"Preço atual: R$ {price:.5}")
		print(f"Preço teto: R$ {max_price:.5}")
		print(f"Diferença de preços R$ {diff:.5}")
		print(f"Média: {avg:.5}")
