
from xadmin.sites import site
from xadmin.views import ListAdminView

from assetprice.models import AssetEarningHistory
from assetprice.plugins import ListHistoryGroupAdmin


class AssetEarningHistoryAdmin:
	list_display = ("ticker", "paid", "year")
	search_fields = ("ticker", "year")
	list_filter = ("year",)
	list_history_grouped = True


site.register(AssetEarningHistory, AssetEarningHistoryAdmin)
site.register_plugin(ListHistoryGroupAdmin, ListAdminView)
