from src.thirdparty.service import Service
from src.thirdparty.tariff import Tariff
from tests.stubs.unit_based_tariff_stub import UnitBasedTariffStub


class ServiceStub(Service):

    def get_tariffs(self) -> list[Tariff]:
        return [UnitBasedTariffStub()]
