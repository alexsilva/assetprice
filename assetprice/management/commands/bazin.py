import argparse
import cloudscraper
import requests
import statistics
from decimal import Decimal
from django.core.management import BaseCommand
from django.utils.module_loading import import_string
from requests import Session

from assetprice import settings
from assetprice.utils import SearchPayLoad, EarningPayLoad


class Ticker:
	def __call__(self, value):
		try:
			if isinstance(settings.TICKER_VALIDATOR, str):
				validator = import_string(settings.TICKER_VALIDATOR)
				value = validator(value and value.upper()).lower()
			return value
		except ValueError as exc:
			raise argparse.ArgumentTypeError(str(exc))


class Command(BaseCommand):
	"""O comando calcula o preço teto com base na fórmula do Décio Bazin"""
	headers = {
		"Cache-Control": "no-cache",
		"Pragma": "no-cache"
	}

	def add_arguments(self, parser):
		parser.add_argument('-t', '--ticker', type=Ticker())

	@classmethod
	def get_price(cls, session: Session, ticker: str):
		resp = session.get(settings.SEARCH_URL, data=SearchPayLoad(ticker).payload, headers=cls.headers)
		if resp.status_code == requests.codes.ok:
			json_data = resp.json()
			price = json_data[0]['price']
			price = price.replace(',', '.')
			price = Decimal(price)
			return price

	@classmethod
	def get_max_price(cls, session: Session, ticker: str):
		resp = session.get(settings.EARNING_URL, data=EarningPayLoad(ticker).payload, headers=cls.headers)
		if resp.status_code == requests.codes.ok:
			json_data = resp.json()
			yearly = json_data['assetEarningsYearlyModels']
			avg = statistics.mean([item['value'] for item in yearly])
			price = Decimal(avg) * settings.BAZIN_TAX
			return price, avg

	def get_data(self, ticker: str):
		"""Extra e calcula o preço teto"""
		data = {}
		with cloudscraper.create_scraper() as scraper:
			price = self.get_price(scraper, ticker)
			max_price, avg = self.get_max_price(scraper, ticker)
			data['price'] = price
			data['max_price'] = max_price
			data['diff'] = max_price - price
			data['avg'] = avg
		return data

	def handle(self, *args, **options):
		""""""
		ticker = options['ticker']
		print("Código: ", ticker, file=self.stdout)

		data = self.get_data(ticker)

		price = data['price']
		max_price = data['max_price']
		diff = data['diff']
		avg = data['avg']

		print(f"Taxa aplicada: {settings.BAZIN_TAX:.5}", file=self.stdout)
		print(f"Preço atual: R$ {price:.5}")
		print(f"Preço teto: R$ {max_price:.5}")
		print(f"Diferença de preços R$ {diff:.5}")
		print(f"Média: {avg:.5}")
