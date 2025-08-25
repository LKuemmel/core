import logging
from control import data
from helpermodules.broker import BrokerClient
from helpermodules.logger import ModifyLoglevelContext
from helpermodules.pub import Pub
from helpermodules.timecheck import create_timestamp
from dataclass_utils import asdict
from helpermodules.utils.topic_parser import decode_payload
from modules.common.abstract_io import AbstractIoAction
from modules.io_actions.controllable_consumers.dimming.config import DimmingSetup

log = logging.getLogger(__name__)
control_command_log = logging.getLogger("steuve_control_command")


class DimmingEebus(AbstractIoAction):
    def __init__(self, config: DimmingSetup):
        self.config = config
        self.import_power_left = None
        # if binary thread running:
        #     control_command_log.info(f"Dimmen per EMS: Steuerbox-Signale werden über EEbus empfangen.")
        # else:
        #     control_command_log.warning("Dimmen per EMS: Steuerbox-Signale können nicht über EEbus empfangen werden.")

        fixed_import_power = 0
        for device in self.config.configuration.devices:
            if device["type"] != "cp":
                fixed_import_power += 4200
        log.debug(f"Dimmen per EMS: Fest vergebene Mindestleistung: {fixed_import_power}W")
        if fixed_import_power != self.config.configuration.fixed_import_power:
            self.config.configuration.fixed_import_power = fixed_import_power
            Pub().pub(f"openWB/set/io/action/{self.config.id}/config", asdict(self.config))

        super().__init__()

    def setup(self) -> None:
        surplus = data.data.counter_data[data.data.counter_all_data.get_evu_counter_str()].calc_raw_surplus()
        if surplus > 0:
            self.import_power_left = self.received_topics["openWB/mqtt/eebus/get/lpc/value"] + surplus
        else:
            self.import_power_left = self.received_topics["openWB/mqtt/eebus/get/lpc/value"]
        self.import_power_left -= self.config.configuration.fixed_import_power
        log.debug(f"Dimmen: {self.import_power_left}W inkl. Überschuss")

        def on_connect(client, userdata, flags, rc):
            client.subscribe(f"openWB/mqtt/eebus/get/lpc/+")

        def on_message(client, userdata, message):
            self.received_topics.update({message.topic: decode_payload(message.payload)})

        self.received_topics = {}
        BrokerClient(f"subscribeMqttEebusAction",
                     on_connect, on_message).start_finite_loop()

        with ModifyLoglevelContext(control_command_log, logging.DEBUG):
            if self.received_topics["openWB/mqtt/eebus/get/lpc/active"]:
                if self.timestamp is None:
                    Pub().pub(f"openWB/set/io/action/{self.config.id}/timestamp", create_timestamp())
                    control_command_log.info("Dimmen aktiviert. Leistungswerte vor Ausführung des Steuerbefehls:")

                msg = (f"EVU-Zähler: "
                       f"{data.data.counter_data[data.data.counter_all_data.get_evu_counter_str()].data.get.powers}W")
                for device in self.config.configuration.devices:
                    if device["type"] == "cp":
                        cp = f"cp{device['id']}"
                        msg += (f", Ladepunkt {data.data.cp_data[cp].data.config.name}: "
                                f"{data.data.cp_data[cp].data.get.powers}W")
                    if device["type"] == "io":
                        io = f"io{device['id']}"
                        msg += (f", {data.data.system_data[io].config.name}: "
                                "Leistung unbekannt")
                control_command_log.info(msg)
            elif self.timestamp:
                Pub().pub(f"openWB/set/io/action/{self.config.id}/timestamp", None)
                control_command_log.info("Dimmen deaktiviert.")

    def dimming_get_import_power_left(self) -> None:
        if self.dimming_active():
            return self.import_power_left
        else:
            return None

    def dimming_set_import_power_left(self, used_power: float) -> None:
        self.import_power_left -= used_power
        log.debug(f"verbleibende Dimm-Leistung: {self.import_power_left}W inkl. Überschuss")
        return self.import_power_left

    def dimming_active(self) -> bool:
        return self.received_topics["openWB/mqtt/eebus/get/lpc/active"]
