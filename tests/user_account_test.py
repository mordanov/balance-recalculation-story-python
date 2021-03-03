import unittest

from src.user_account import UserAccount
from tests.stubs.balance_spy import BalanceSpy
from tests.stubs.calculation_history_for_multi_service_stub import CalculationHistoryForMultiServiceStub
from tests.stubs.calculation_history_service_stub import CalculationHistoryServiceStub
from tests.stubs.date_creator import DateCreator
from tests.stubs.multi_tariff_service_stub import MultiTariffServiceStub
from tests.stubs.no_rate_tariff_stub import NoRateTariffStub
from tests.stubs.second_service_stub import SecondServiceStub
from tests.stubs.service_stub import ServiceStub
from tests.stubs.unit_based_tariff_stub import UnitBasedTariffStub


class UnitAccountTest(unittest.TestCase):
    UNIT_RATE = 0.8
    serviceStub = ServiceStub()
    multi_tariff_service_stub = MultiTariffServiceStub([UnitBasedTariffStub(), NoRateTariffStub()])
    balance_spy: object
    user_account = UserAccount()

    def setUp(self):
        self.setup_payment_date()
        self.balance_spy = BalanceSpy()
        self.user_account.balance = self.balance_spy
        self.user_account.services = [self.serviceStub]

    def setup_payment_date(self):
        self.user_account.payment_dates = {
            DateCreator.create_date(2001, 3, 22),
            DateCreator.create_date(2001, 2, 23),
            DateCreator.create_date(2001, 5, 19),
        }

    def test_should_not_apply_payment_when_all_fees_already_recalculated(self):
        self.setup_uncalculated_fees({})
        self.user_account.recalculate_balance()
        self.verify_applied_sum(0.0)

    def test_should_apply_sum_of_all_not_calculated_fees(self):
        self.setup_uncalculated_fees({
            DateCreator.create_date(2001, 5, 20): 200.0,
            DateCreator.create_date(2001, 6, 22): 150.0,
        })
        self.user_account.recalculate_balance()
        self.verify_applied_sum(350.0 * self.UNIT_RATE)

    def test_should_apply_sum_for_tariff_with_highest_rate(self):
        self.user_account.services = [self.multi_tariff_service_stub]
        self.setup_uncalculated_fees({
            DateCreator.create_date(2001, 5, 20): 200.0,
            DateCreator.create_date(2001, 6, 22): 150.0,
        })
        self.user_account.recalculate_balance()
        self.verify_applied_sum(350.0)

    def test_should_apply_sum_for_tariff_with_additional_fee_for_each_uncalculated_fee(self):
        self.setup_tariffs([NoRateTariffStub(10.0), NoRateTariffStub()])
        self.setup_uncalculated_fees({
            DateCreator.create_date(2001, 5, 20): 200.0,
            DateCreator.create_date(2001, 6, 22): 150.0,
        })
        self.user_account.recalculate_balance()
        self.verify_applied_sum(350.0 + 10.0 + 10.0)

    def test_should_apply_sum_for_tariff_with_additional_fee_when_its_higher_then_other_tariff(self):
        self.setup_tariffs([NoRateTariffStub(), UnitBasedTariffStub(50.0)])
        self.setup_uncalculated_fees({
            DateCreator.create_date(2001, 5, 20): 200.0,
        })
        self.user_account.recalculate_balance()
        self.verify_applied_sum(200.0 * self.UNIT_RATE + 50.0)

    def test_should_apply_sum_for_tariff_with_highest_rate_when_its_higher_then_other_tariff(self):
        self.setup_tariffs([NoRateTariffStub(), UnitBasedTariffStub(10.0)])
        self.setup_uncalculated_fees({
            DateCreator.create_date(2001, 5, 20): 200.0,
        })
        self.user_account.recalculate_balance()
        self.verify_applied_sum(200.0)

    def test_should_apply_sum_of_all_not_calculated_fees_for_all_services(self):
        # given
        self.user_account.services = [ServiceStub(), SecondServiceStub()]
        calc_history_service = CalculationHistoryForMultiServiceStub({
            DateCreator.create_date(2001, 5, 20): 200.0,
        },
            {
                DateCreator.create_date(2001, 7, 25): 120.0,
                DateCreator.create_date(2001, 6, 25): 180.0,
            })
        self.user_account.calc_history_service = calc_history_service

        # when
        self.user_account.recalculate_balance()

        # then
        calc_history_service.verify_applied_sum_for_service(200.0 * self.UNIT_RATE, ServiceStub.__name__)
        calc_history_service.verify_applied_sum_for_service((120.0 + 180.0) * self.UNIT_RATE,
                                                            SecondServiceStub.__name__)
        self.balance_spy.verify_updated_sum((200.0 + 120.0 + 180.0) * self.UNIT_RATE)

    def setup_tariffs(self, tariffs):
        self.user_account.services = [MultiTariffServiceStub(tariffs)]

    def setup_uncalculated_fees(self, uncalculated_fees):
        self.calculation_history_service_stub = CalculationHistoryServiceStub(uncalculated_fees)
        self.user_account.calc_history_service = self.calculation_history_service_stub

    def verify_applied_sum(self, expected_sum):
        self.balance_spy.verify_updated_sum(expected_sum)
        self.calculation_history_service_stub.verify_applied_sum(expected_sum)


if __name__ == "__main__":
    unittest.main()
