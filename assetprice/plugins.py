from django.db.models import Sum, Count
from django.utils.timezone import now
from xadmin.views import BaseAdminPlugin

date_now = now()


class ListHistoryGroupAdmin(BaseAdminPlugin):
	"""Plugin que agrupa os resultados por ativos"""
	list_history_grouped = False
	list_history_interval = 6

	def init_request(self, *args, **kwargs):
		return self.list_history_grouped

	def setup(self, *args, **kwargs):
		self.index = 1
		self.ordering_map = {
			'paid': "paid__sum",
			'year': "year__count"
		}

	def queryset(self, qs):
		qs = qs.filter(year__gt=date_now.year - self.list_history_interval)
		qs = qs.values("ticker").distinct().order_by()
		qs = qs.annotate(Sum("paid"), Count("year"))
		return qs

	def get_ordering(self, ordering):
		exclude = ('pk', '-pk')
		for field_name in exclude:
			try:
				ordering.remove(field_name)
			except ValueError:
				continue
		ordering_fields = list(ordering)
		for field_name in ordering_fields:
			direction, field_name = field_name[0], field_name[1:]
			full_name = direction + field_name
			ordering.remove(full_name)
			if direction == '-':
				ordering.append(direction + self.ordering_map.get(field_name, field_name))
			else:
				ordering.append(self.ordering_map.get(full_name, full_name))
		return ordering

	def result_row(self, __, obj):
		if isinstance(obj, self.model):
			return __()

		obj = obj.copy()

		obj[self.opts.pk.attname] = self.index

		self.index += 1

		obj['year'] = obj.pop(self.ordering_map['year'])
		obj['paid'] = obj.pop(self.ordering_map['paid'])

		obj = self.model(**obj)

		return self.admin_view.result_row(obj)
