import time
from datetime import datetime, timedelta
import calendar
import pytz
from pytz import timezone
import time
from datetime import datetime, timedelta



class TimeConvert:
	"""Şimdiki zamanı unix timestapm olarak getiren class."""

	def get_current_time(self):
		now = int(time.time())
		return now

	def convert_to_human_readeble(self, tstamp, frmt=None):
		if not frmt:
			frmt = '%d.%m.%Y-%H:%M:%S'
		turkey = pytz.timezone('Europe/Istanbul')
		return datetime.utcfromtimestamp(tstamp).astimezone(turkey).strftime(frmt)

	def start_or_end_wtih_tz(self, stamp, start_or_end, **kwargs):

		if type(stamp) != int:
			try:
				stamp = int(stamp)
			except:
				raise NotImplementedError('date is not int timestamp')

		zone = kwargs.get('zone', None)
		if not zone:
			zone = "Europe/Istanbul"

		utc = pytz.timezone("UTC")
		as_date = datetime.fromtimestamp(stamp)

		aware_date = utc.localize(as_date)
		_zone = pytz.timezone(zone)
		converted_time_with_zone = aware_date.astimezone(_zone)
		month = kwargs.get('month')
		week = kwargs.get('week')
		if start_or_end == "start":
			converted_time_with_zone = converted_time_with_zone.replace(hour=0, minute=0, second=0)
			if week:
				converted_time_with_zone = converted_time_with_zone - timedelta(days=converted_time_with_zone.weekday() % 7)
			if month:
				converted_time_with_zone = converted_time_with_zone.replace(day=1)

		elif start_or_end == "end":
			converted_time_with_zone = converted_time_with_zone.replace(hour=23, minute=59, second=59)
			if week:
				start_of_week = converted_time_with_zone - timedelta(days=converted_time_with_zone.weekday() % 7)
				converted_time_with_zone = start_of_week + timedelta(days=6)  # Sunday

			if month:
				_ay = converted_time_with_zone.month
				_yil = converted_time_with_zone.year
				_, _son_gun = calendar.monthrange(_yil, _ay)
				converted_time_with_zone = converted_time_with_zone.replace(day=_son_gun)
		return converted_time_with_zone



if __name__ == '__main__':
    TimeConvert()