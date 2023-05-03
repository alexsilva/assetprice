import statistics
from decimal import Decimal

from django.utils.timezone import now

from assetprice import settings
from . import paid_history
from ._driver import ResponseResult
from ...utils import SearchUrl, EarningUrl


class MaxPrice:
	def __init__(self, value, avg):
		self.value = value
		self.avg = avg


class Command(paid_history.Command):
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
		return cls._get_max_price([item['value'] for item in yearly])

	@classmethod
	def _get_max_price(cls, values) -> MaxPrice:
		avg = statistics.mean([value for value in values])
		price = Decimal(avg) * settings.BAZIN_TAX
		return MaxPrice(price, avg)

	@staticmethod
	def get_url(url, payload):
		return url + "?" + payload.data

	def get_spec(self, ticker, **options):
		"""Extra e calcula o preço teto"""
		response = self.get_json(str(SearchUrl(ticker)))
		if options['verbosity'] > 2:
			print(response)
		price = self.get_price(response)

		interval = 5
		date_now = now()
		queryset = self.get_from_history(ticker, date_now.year - interval, date_now.year)
		if queryset.count() >= interval:
			max_price = self._get_max_price([item.paid for item in queryset])
		else:
			response = self.get_json(str(EarningUrl(ticker)))
			if options['verbosity'] > 2:
				print(response)

			max_price = self.get_max_price(response)
			if max_price.value > 0:
				self.save_history(ticker, response, **options)

		data = {
			'price': price,
			'max_price': max_price,
			'diff': max_price.value - price,
		}
		return data

	def handle(self, *args, **options):
		""""""
		ticker = options.pop('ticker')
		print("Código: ", ticker, file=self.stdout)

		data = self.get_spec(ticker, **options)
		price = data['price']
		max_price = data['max_price']
		diff = data['diff']

		print(f"Taxa aplicada: {settings.BAZIN_TAX:.5}", file=self.stdout)
		print(f"Preço atual: R$ {price:.5}", file=self.stdout)
		print(f"Preço teto: R$ {max_price.value:.5}", file=self.stdout)
		print(f"Diferença de preços R$ {diff:.5}", file=self.stdout)
		print(f"Média: {max_price.avg:.5}", file=self.stdout)
