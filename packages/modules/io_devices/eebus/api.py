#!/usr/bin/env python3
from pathlib import Path
import logging
from threading import Thread

from control import data
from helpermodules.broker import BrokerClient
from helpermodules.pub import pub_single
from helpermodules.utils.run_command import run_command
from helpermodules.utils._thread_handler import is_thread_alive, thread_handler
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

cert_path = f"{Path(__file__).resolve().parents[2]}/data/config/eebus/certs"


def create_io(config: Eebus):
    received_topics = {}
    broker = None

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
                control_command_log.error(f"Fehler im EEbus-Client: {e}")
                raise e

    def read():
        nonlocal broker
        nonlocal received_topics
        if is_thread_alive("eebus_binary"):
            run_eebus()
        log.debug(f"Empfange MQTT Daten für Eebus {config.id}: {received_topics}")
        broker.start_finite_loop()
        try:
            return IoState(
                analog_input={
                    AnalogInputMapping.LPC_VALUE.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpc"]["limit"],
                    AnalogInputMapping.LPC_MSG_COUNTER.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpc"]["msgCounter"],
                    AnalogInputMapping.LPP_VALUE.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpp"]["limit"],
                    AnalogInputMapping.LPP_MSG_COUNTER.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpp"]["msgCounter"],
                },
                digital_input={DigitalInputMapping.LPC_ACTIVE.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpc"]["isLimitActive"],
                               DigitalInputMapping.LPP_ACTIVE.name: received_topics[f"openWB/mqtt/eebus/{config.id}/get/lpp"]["isLimitActive"]})
        except KeyError:
            raise KeyError("Es konnten keine Daten von der Steuerbox mit EEbus-Schnittstelle empfangen werden. ")

    def write():
        # antwort auf LPC?
        pass

    def initializer():
        nonlocal broker
        nonlocal received_topics
        thread_handler(Thread(
            target=run_eebus,
            args=(),
            name="eebus_binary"))

        def on_connect(client, userdata, flags, rc):
            client.subscribe(f"openWB/mqtt/eebus/{config.id}/get/#")

        def on_message(client, userdata, message):
            received_topics.update({message.topic: decode_payload(message.payload)})

        received_topics = {}
        broker = BrokerClient(f"subscribeMqttEebus{config.id}",
                              on_connect, on_message)

    return ConfigurableIo(config=config, component_reader=read, component_writer=write, initializer=initializer)


device_descriptor = DeviceDescriptor(configuration_factory=Eebus)


def create_pub_cert_ski(id: int):
    Path(cert_path).mkdir(parents=True, exist_ok=True)
    run_command([
        "openssl", "genrsa", "-out", f"{cert_path}/hems-key-{id}.pem", "2048"
    ])
    run_command([
        "openssl", "req", "-new", "-x509",
        "-key", f"{cert_path}/hems-key-{id}.pem",
        "-out", f"{cert_path}/hems-cert-{id}.pem",
        "-days", "365",
        "-subj", "/CN=HEMS/C=DE/O=openWB GmbH"
    ])

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
    config: Eebus = data.data.system_data[f"io{id}"].configuration
    config.configuration.cert_info = cert_info
    with open(f"{cert_path}/ski-{id}", "w") as ski_file:
        ski_file.write(cert_info.ski)
    pub_single(f"openWB/set/openWB/system/io/{config.id}/config", config)
