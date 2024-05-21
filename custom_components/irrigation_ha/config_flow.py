"""Config flow for integration."""
from __future__ import annotations

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
)
from homeassistant.components.input_boolean import (
    DOMAIN as INPUT_BOOLEAN_DOMAIN,
)
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_COUNT
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.helpers import selector

from . import const as irri


class IrrigationHaFlow(ConfigFlow, domain=irri.DOMAIN):
    """
    Irrigation HA config flow
    """

    async def async_step_user(
            self, user_input,
    ):
        """
        Init step
        """

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_ENTITY_ID],
                data=user_input,
            )

        return self.async_show_form(
            data_schema=vol.Schema({
                vol.Required(CONF_COUNT, default=1): cv.positive_int,
                vol.Required(CONF_ENTITY_ID): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain=[
                            SWITCH_DOMAIN,
                            INPUT_BOOLEAN_DOMAIN,
                            BINARY_SENSOR_DOMAIN,
                        ], multiple=False,
                    ),
                ),
            }),
        )
