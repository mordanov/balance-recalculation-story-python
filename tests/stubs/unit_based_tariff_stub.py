from src.thirdparty.tariff import Tariff
from src.thirdparty.tariff_type import TariffType


class UnitBasedTariffStub(Tariff):

    def __init__(self, additional_fee=None):
        self.additional_fee = 0 if additional_fee is None else additional_fee

    def get_additional_fee(self):
        return self.additional_fee

    def get_type(self) -> TariffType:
        return UnitBasedTariffTypeStub()


class UnitBasedTariffTypeStub(TariffType):

    def is_unit_based(self):
        return True
