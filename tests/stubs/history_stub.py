import unittest

from src.thirdparty.history import History
from src.thirdparty.service import Service
from src.thirdparty.tariff import Tariff
from tests.stubs.date_creator import DateCreator


class HistoryStub(History, unittest.TestCase):
    DELTA = 0.0001
    fees: dict = {}

    def __init__(self, uncalculated_fees):
        super().__init__()
        self.applied_sum = 0
        self.fees = self.get_calculated_fees()
        self.fees.update(uncalculated_fees)

    def get_all_fees(self, tariff: Tariff, service: Service):
        return self.fees

    def get_calculated_fees(self):
        return {DateCreator.create_date(2001, 4, 28): 100.0,
                DateCreator.create_date(2001, 5, 18): 150.0}

    def apply_recalculation(self, value, unit_rate):
        self.applied_sum = value
        from tests.user_account_test import UnitAccountTest
        self.assertAlmostEqual(UnitAccountTest.UNIT_RATE, unit_rate, delta=self.DELTA)

    def verify_applied_sum(self, expected_sum):
        self.assertAlmostEqual(expected_sum, self.applied_sum, delta=self.DELTA)
