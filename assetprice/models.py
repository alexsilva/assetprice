from decimal import Decimal

from django.db import models


class AssetEarningHistory(models.Model):
	ticker = models.CharField(verbose_name="Código", max_length=8)
	year = models.PositiveIntegerField(verbose_name="Ano")
	paid = models.DecimalField(verbose_name="Valor pago",
	                           max_digits=28,
	                           decimal_places=4,
	                           default=Decimal(0))

	class Meta:
		verbose_name = "Histórico de proventos"
		ordering = ("ticker", "year")

	def __str__(self):
		return f"{self.ticker}: {self.year} R$ {self.paid}"
