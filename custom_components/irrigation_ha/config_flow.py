"""Config flow for integration."""
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME

from . import const as irri


class IrrigationHaFlow(ConfigFlow, domain=irri.DOMAIN):
    """
    Irrigation HA config flow
    """

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """
        Init step
        """

        errors = {}

        if user_input is not None:
            irri.LOGGER.info('Gathering mac address')

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )
