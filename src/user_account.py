import datetime

from src.thirdparty.balance import Balance
from src.thirdparty.calculation_history_service import CalculationHistoryService
from src.thirdparty.service import Service


class UserAccount:
    EPOCH_TIMESTAMP = datetime.datetime(1970, 1, 1)
    UNIT_RATE = 0.8

    def __init__(self):
        self.balance = Balance()
        self.payment_dates: list[datetime.datetime] = []
        self._services: list[Service] = []
        self._calc_history_service = CalculationHistoryService()

    def recalculate_balance(self):
        for service in self._services:
            self.recalculate_service(service)

    def recalculate_service(self, service):
        history = self._calc_history_service.retrieve_history(service)
        self.pay_tariff(history, self.get_highest_tariff(service, history))

    def pay_tariff(self, history, highest_tariff):
        history.apply_recalculation(highest_tariff, self.UNIT_RATE)
        self.balance.update_balance(highest_tariff)

    def get_highest_tariff(self, service, history):
        tariffs = service.get_tariffs()
        highest_tariff = 0
        for tariff in tariffs:
            highest_tariff = max(highest_tariff, self.calculate_unapplied(tariff, history.get_all_fees(tariff, service)))
        return highest_tariff

    def calculate_unapplied(self, tariff, fees):
        calculated_sum = 0.0
        for date in fees.keys():
            if date > self.get_last_calculation_date():
                calculated_sum += fees.get(date) * self.get_rate(tariff) + tariff.get_additional_fee()
        return calculated_sum

    def get_last_calculation_date(self):
        latest = self.EPOCH_TIMESTAMP
        for p in self.payment_dates:
            latest = p if p.timestamp() > latest.timestamp() else latest
        return latest

    def get_rate(self, tariff):
        return self.UNIT_RATE if tariff.get_type().is_unit_based() else 1

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
