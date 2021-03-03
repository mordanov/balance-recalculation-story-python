from src.thirdparty.calculation_history_service import CalculationHistoryService
from src.thirdparty.history import History
from src.thirdparty.service import Service
from tests.stubs.history_stub import HistoryStub
from tests.stubs.second_service_stub import SecondServiceStub
from tests.stubs.service_stub import ServiceStub


class CalculationHistoryForMultiServiceStub(CalculationHistoryService):
    history_map: dict = {}

    def __init__(self, uncalculated_fees, second_uncalculated_fees):
        self.history_map[ServiceStub.__name__] = HistoryStub(uncalculated_fees)
        self.history_map[SecondServiceStub.__name__] = HistoryStub(second_uncalculated_fees)

    def retrieve_history(self, service: Service) -> History:
        return self.history_map.get(service.__class__.__name__)

    def verify_applied_sum_for_service(self, expected_sum, service_class):
        self.history_map.get(service_class).verify_applied_sum(expected_sum)
