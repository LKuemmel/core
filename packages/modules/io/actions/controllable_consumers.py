from helpermodules.pub import Pub


def direct_control_cp(input_state: bool, cp_num: int) -> None:
    # pub state to cp
    pass


def dim(input_state: bool) -> None:
    Pub().pub("openWB/set/general/ripple_control_receiver/get/active", input_state)


def ripple_control_receiver(input_state: bool) -> None:
    # pub state to ripple_control
    pass


CONTROLLABLE_CONSUMERS_ACTIONS = [{"action": "dim", "action_parameters": []},
                                  {"action": "ripple_control_receiver", "action_parameters": []},
                                  {"action": "direct_control_cp", "action_parameters": ["cp_num"]},]
