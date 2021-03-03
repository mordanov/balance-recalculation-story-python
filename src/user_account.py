import datetime

from src.thirdparty.balance import Balance
from src.thirdparty.calculation_history_service import CalculationHistoryService
from src.thirdparty.service import Service


class UserAccount:
    EPOCH_TIMESTAMP = datetime.datetime(1970, 1, 1)

    def __init__(self):
        self.balance = Balance()
        self.payment_dates: list[datetime.datetime] = []
        self._services: list[Service] = []
        self._calc_history_service = CalculationHistoryService()

    def recalculate_balance(self):
        unit_rate = 0.8

        for service in self._services:
            tariffs = service.get_tariffs()
            h = self._calc_history_service.retrieve_history(service)

            # find last calculation date
            latest = self.EPOCH_TIMESTAMP
            for p in self.payment_dates:
                latest = p if p.timestamp() > latest.timestamp() else latest
            d = latest

            highest_tariff = 0.0
            if tariffs:
                for tariff in tariffs:
                    tariff_type = tariff.get_type()
                    highest_tariff = max(highest_tariff,
                                         self.calculate_unapplied(tariff, d, h, unit_rate, tariff_type, service))

            h.apply_recalculation(highest_tariff, unit_rate)
            self.balance.update_balance(highest_tariff)

    def calculate_unapplied(self, tariff, last_calculation_date, h, unit_rate, t, service):
        fees: dict = h.get_all_fees(tariff, service)
        sum = 0.0
        for date in fees.keys():
            if date > last_calculation_date:
                sum += fees.get(date) * (unit_rate if (t.is_unit_based()) else 1) + tariff.get_additional_fee()
        return sum

    @property
    def calc_history_service(self):
        return self._calc_history_service

    @property
    def services(self):
        return self._services

    @calc_history_service.setter
    def calc_history_service(self, calc_history_service):
        self._calc_history_service = calc_history_service

    @services.setter
    def services(self, services):
        self._services = services
