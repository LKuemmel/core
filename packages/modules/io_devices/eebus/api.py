#!/usr/bin/env python3
from pathlib import Path
import logging
from threading import Thread

from helpermodules.broker import BrokerClient
from helpermodules.pub import pub_single
from helpermodules.utils import run_command
from helpermodules.utils._thread_handler import thread_handler
from helpermodules.utils.topic_parser import decode_payload
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import IoState
from modules.common.component_type import ComponentType
from modules.common.configurable_io import ConfigurableIo
from modules.common.fault_state import ComponentInfo, FaultState
from modules.io_devices.eebus.config import AnalogInputMapping, CertInfo, DigitalInputMapping, Eebus

log = logging.getLogger(__name__)
control_command_log = logging.getLogger("steuve_control_command")


def create_io(config: Eebus):
    received_topics = {}
    cert_path = f"{Path(__file__).resolve().parents[2]}/data/config/eebus/certs"

    def run_eebus():
        with SingleComponentUpdateContext(FaultState(ComponentInfo(config.id, config.name, ComponentType.IO.value))):
            try:
                run_command(
                    ["./eebus_hems_client", "port",
                     f"{cert_path}/ski-{config.id}",
                        f"{cert_path}/hems-cert-{config.id}.pem",
                        f"{cert_path}/hems-key-{config.id}.pem"],
                    config.id
                )
            except Exception as e:
                control_command_log.error(f"Dimmen per EMS: Fehler im EEbus-Client: {e}")
                raise e

    def read():
        nonlocal received_topics
        log.debug(f"Empfange MQTT Daten für Eebus {config.id}: {received_topics}")
        try:
            return IoState(
                analog_input={
                    AnalogInputMapping.VALUE.name: received_topics["openWB/mqtt/eebus/get/lpc/value"]},
                digital_input={DigitalInputMapping.ACTIVE.name: received_topics["openWB/mqtt/eebus/get/lpc/active"]})
        except KeyError:
            raise KeyError("Es konnten keine Daten von der Steuerbox mit EEbus-Schnittstelle empfangen werden. ")

    def initializer():
        nonlocal received_topics
        # create certificate
        # extract ski
        # pub ski
        # start binary wich connects to controlbox and publishes lpc and lpp signals
        create_certificate()
        extract_cert_info()
        thread_handler(Thread(
            target=run_eebus,
            args=(),
            name="eebus_binary"))

        def on_connect(client, userdata, flags, rc):
            client.subscribe(f"openWB/mqtt/eebus/{config.id}/get/#")

        def on_message(client, userdata, message):
            received_topics.update({message.topic: decode_payload(message.payload)})

        received_topics = {}
        BrokerClient(f"subscribeMqttEebus{config.id}",
                     on_connect, on_message).start_finite_loop()

    def create_certificate():
        run_command([
            "openssl", "genrsa", "-out", f"{cert_path}/hems-key-{config.id}.pem", "2048"
        ])
        run_command([
            "openssl", "req", "-new", "-x509",
            "-key", f"{cert_path}/hems-key-{config.id}.pem",
            "-out", f"{cert_path}/hems-cert-{config.id}.pem",
            "-days", "365",
            "-subj", "/CN=HEMS/C=DE/O=openWB GmbH"
        ])
        return ConfigurableIo(config=config, component_reader=read, initializer=initializer)

    def extract_cert_info(cert_path: str) -> dict:
        output = run_command([
            "openssl", "x509", "-in", cert_path, "-noout", "-text"
        ])
        cert_info = CertInfo()
        lines = output.splitlines()
        for i, line in enumerate(lines):
            if "Subject Key Identifier" in line:
                cert_info.ski = lines[i+1].strip().replace(":", "")
            elif "Not Before:" in line:
                cert_info.not_before = line.split("Not Before: ")[1].strip()
            elif "Not After :" in line:
                cert_info.not_after = line.split("Not After: ")[1].strip()
            elif line.strip().startswith("Issuer:"):
                cert_info.issuer = line.strip()[len("Issuer: "):].strip()
            elif line.strip().startswith("Subject:"):
                cert_info.subject = line.strip()[len("Subject: "):].strip()
        if "" == cert_info.ski:
            raise ValueError("SKI nicht gefunden")
        config.configuration.cert_info = cert_info
        with open(f"{cert_path}/ski-{config.id}", "w") as ski_file:
            ski_file.write(cert_info.ski)
        pub_single("/config", config)

    return ConfigurableIo(config=config, component_reader=read, initializer=initializer)


device_descriptor = DeviceDescriptor(configuration_factory=Eebus)
