import unittest

from src.thirdparty.balance import Balance
from tests.stubs.history_stub import HistoryStub


class BalanceSpy(Balance, unittest.TestCase):
    updated_sum = 0.0

    def update_balance(self, sum):
        self.updated_sum += sum

    def verify_updated_sum(self, expected_sum):
        self.assertAlmostEqual(expected_sum, self.updated_sum, delta=HistoryStub.DELTA)
