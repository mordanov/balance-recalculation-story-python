from src.thirdparty.service import Service
from src.thirdparty.tariff import Tariff


class MultiTariffServiceStub(Service):

    def __init__(self, tariffs):
        self.tariffs = tariffs

    def get_tariffs(self) -> list[Tariff]:
        return self.tariffs
