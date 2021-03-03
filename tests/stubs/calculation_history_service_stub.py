from src.thirdparty.calculation_history_service import CalculationHistoryService
from src.thirdparty.history import History
from src.thirdparty.service import Service
from tests.stubs.history_stub import HistoryStub


class CalculationHistoryServiceStub(CalculationHistoryService):

    def __init__(self, uncalculated_fees):
        self.history_stub = HistoryStub(uncalculated_fees)

    def retrieve_history(self, service: Service) -> History:
        return self.history_stub

    def verify_applied_sum(self, expected_sum):
        self.history_stub.verify_applied_sum(expected_sum)
