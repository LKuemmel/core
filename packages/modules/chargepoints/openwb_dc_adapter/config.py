from typing import Optional

from helpermodules import hardware_configuration
from modules.common.abstract_chargepoint import SetupChargepoint


class AlpitronicHypercharger:
    def __init__(self,
                 load_sharing_max: float = 150,
                 load_sharing_shared: float = 75,
                 laodsharing_partner_ip: str = None):
        self.name = "alpitronic Hypercharger"
        self.load_sharing_max = load_sharing_max
        self.load_sharing_shared = load_sharing_shared
        self.laodsharing_partner_ip = laodsharing_partner_ip


def alpitronic_hypercharger_factory():
    return AlpitronicHypercharger()


class OpenWBDcAdapterConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 station: AlpitronicHypercharger = alpitronic_hypercharger_factory()):
        self.ip_address = ip_address
        self.station = station


class OpenWBDcAdapter(SetupChargepoint[OpenWBDcAdapterConfiguration]):
    def __init__(self,
                 name: str = "openWB Adapter für DC-Lader",
                 type: str = "openwb_dc_adapter",
                 id: int = 0,
                 configuration: OpenWBDcAdapterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or OpenWBDcAdapterConfiguration())
        self.visibility = hardware_configuration.get_hardware_configuration_setting("dc_charging")
        self.charging_type = "DC"
