#!/usr/bin/env python3
from helpermodules.broker import BrokerClient
from helpermodules.utils import run_command
from helpermodules.utils.topic_parser import decode_payload
from modules.common.configurable_io import ConfigurableIo
from modules.io_devices.eebus.config import Eebus
import logging

from modules.common.abstract_device import DeviceDescriptor

log = logging.getLogger(__name__)


VALID_VERSIONS = ["openWB DimmModul"]


def create_io(config: Eebus):
    def run_eebus():
        with SingleComponentUpdateContext(self.fault_state):
            run_command(
                ["binary", "port", "server", "ski", "client-cert", "client-key"]
            )
        error_handler

    def read():
        def on_connect(client, userdata, flags, rc):
            client.subscribe(f"openWB/mqtt/eebus/get/#")

        def on_message(client, userdata, message):
            received_topics.update({message.topic: decode_payload(message.payload)})

        received_topics = {}
        BrokerClient(f"subscribeMqttEebus{config.id}",
                     on_connect, on_message).start_finite_loop()

        if received_topics:
            log.debug(f"Empfange MQTT Daten für Eebus {config.id}: {received_topics}")

    def initializer():
        # create certificate
        # extract ski
        # pub ski
        # start binary wich connects to controlbox and publishes lpc and lpp signals
        thread_handler(Thread(
            target=run_eebus,
            args=(),
            name="eebus_binary"))

        pass
    return ConfigurableIo(config=config, component_reader=read, initializer=initializer)


device_descriptor = DeviceDescriptor(configuration_factory=Eebus)
