import datetime


class DateCreator:

    @staticmethod
    def create_date(year, month, date):
        return datetime.datetime(year=year, month=month, day=date)
