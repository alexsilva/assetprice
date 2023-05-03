from xadmin.sites import site

from assetprice.models import AssetEarningHistory


class AssetEarningHistoryAdmin:
	list_display = ("ticker", "paid", "year")
	search_fields = ("ticker", "year")
	list_filter = ("year",)


site.register(AssetEarningHistory, AssetEarningHistoryAdmin)
