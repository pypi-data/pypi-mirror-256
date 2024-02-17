import threading
from typing import Protocol, cast

from .session_state import SessionState


class StatesHolder(Protocol):
    _states: dict[str, SessionState]
    _state_lock: threading.Lock


class MainThread(StatesHolder, threading.Thread):
    pass


def init_main_thread() -> None:
    thread = main_thread()
    if not hasattr(thread, "_states"):
        thread._states = {}
        thread._state_lock = threading.Lock()


def main_thread() -> MainThread:
    return cast(MainThread, threading.main_thread())


def state_lock() -> threading.Lock:
    return main_thread()._state_lock


def fresh_state(ident: str) -> SessionState:
    if ident in get_states():
        old = get_states()[ident]
        old.__del__()

    return _get_state(ident)


def get_states() -> dict[str, SessionState]:
    return main_thread()._states


def set_states(states: dict[str, SessionState]):
    with state_lock():
        main_thread()._states = states


def set_state(ident: str, state: SessionState) -> None:
    get_states().update({ident: state})


def _get_state(ident: str) -> SessionState:
    if state := get_states().get(ident):
        return state

    state = SessionState(ident)
    get_states().update({ident: state})

    return state


def drop_state(ident: str) -> None:
    if ident in get_states():
        with state_lock():
            get_states().pop(ident)


def close_state(state: SessionState) -> None:
    try:
        state.clear()
    finally:
        drop_state(state.ident)
        del state
