from helpermodules.pub import Pub


def dimming_via_direct_control(input_state: bool, cp_num: int) -> None:
    Pub().pub(f"openWB/set/chargepoint/{cp_num}/get/dimming_via_direct_control", input_state)


def dimming(input_state: bool) -> None:
    Pub().pub("openWB/set/general/dimming/get/active", input_state)


def ripple_control_receiver(input_state: bool) -> None:
    Pub().pub("openWB/set/general/ripple_control_receiver/get/active", input_state)


CONTROLLABLE_CONSUMERS_ACTIONS = [{"action": "dimming", "action_parameters": []},
                                  {"action": "ripple_control_receiver", "action_parameters": []},
                                  {"action": "dimming_via_direct_control", "action_parameters": ["cp_num"]},]
