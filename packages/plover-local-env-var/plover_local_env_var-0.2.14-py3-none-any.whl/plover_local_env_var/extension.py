"""
Plover entry point extension module for Plover Local Env Var.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/meta.html
"""
from pathlib import Path

from plover.engine import StenoEngine
from plover.formatting import _Action, _Context
from plover.machine.base import STATE_RUNNING
from plover.oslayer.config import CONFIG_DIR
from plover.registry import registry

from . import config
from . import env_var


_CONFIG_FILEPATH = Path(CONFIG_DIR) / "local_env_var.json"

class LocalEnvVar:
    """
    Extension class that also registers a meta plugin.
    The meta deals with fetching local env var values.
    """
    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine
        self._env_var_values: dict[str, str] = {}

    def start(self) -> None:
        """
        Sets up the meta plugin and steno engine hooks
        """
        registry.register_plugin("meta", "ENV_VAR", self._env_var)
        self._engine.hook_connect(
            "machine_state_changed",
            self._machine_state_changed
        )
        self._env_var_values = config.load(_CONFIG_FILEPATH)

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        self._engine.hook_disconnect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def _env_var(self, ctx: _Context, argument: str) -> _Action:
        """
        Fetches a local env var and stores it in memory for faster
        execution on subsequent calls.
        """
        if not argument:
            raise ValueError("No $ENV_VAR provided")

        try:
            env_var_value = self._env_var_values[argument]
        except KeyError:
            env_var_value = env_var.expand(argument)
            self._env_var_values[argument] = env_var_value
            config.save(
                _CONFIG_FILEPATH,
                sorted(self._env_var_values.keys())
            )

        action = ctx.new_action()
        action.text = env_var_value
        return action

    def _machine_state_changed(
        self,
        _machine_type: str,
        machine_state: str
    ) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed. Resetting the `_env_var_values` dictionary allows for changes
        made to env vars to be re-read in.
        """
        if machine_state == STATE_RUNNING:
            self._env_var_values = config.load(_CONFIG_FILEPATH)
