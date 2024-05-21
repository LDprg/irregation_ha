"""Config flow for integration."""
from __future__ import annotations

from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_COUNT
from homeassistant.const import CONF_ENTITY_ID

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
                vol.Required(CONF_COUNT): cv.positive_int,
                vol.Required(CONF_ENTITY_ID):
                    cv.entity_domain('camera'),
            }),
            errors=errors,
        )
