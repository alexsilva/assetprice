from assetprice.management.commands._driver import BaseWebDriverCommand, ResponseResult
from assetprice.models import AssetEarningHistory
from assetprice.utils import EarningUrl


class Command(BaseWebDriverCommand):
	help = "Salva o histórico de dividendos em anos"
	history_model = AssetEarningHistory

	def save_history(self, ticker: str, response: ResponseResult, **options):
		verbosity = options.get('verbosity', 0)
		for item in response.data['assetEarningsYearlyModels']:
			if verbosity > 1:
				print(item)

			defaults = {'paid': item['value']}
			instance, _ = self.history_model.objects.get_or_create(
				defaults=defaults,
				year=item['rank'],
				ticker=ticker.upper()
			)
			if verbosity > 1:
				print(instance)

	def get_from_history(self, ticker, start, end):
		results = self.history_model.objects.filter(
			ticker__iexact=ticker,
			year__gte=start,
			year__lte=end)
		return results

	def handle(self, *args, **options):
		ticker = options.pop('ticker')
		verbosity = options.get('verbosity', 1)

		response = self.get_json(str(EarningUrl(ticker)))

		if verbosity > 2:
			print(response.data, file=self.stdout)

		if response.data:
			self.save_history(ticker, response, **options)
