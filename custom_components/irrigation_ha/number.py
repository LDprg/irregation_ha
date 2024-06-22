"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import CONF_COUNT

from . import const as irri
from .coordinator import IRRICoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    _config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    coordinator: IRRICoordinator = hass.data[irri.DOMAIN]["coord"]

    async_add_entities(
        [
            IRRINumber(coordinator, name)
            for name in ["stop_duration"]
            + [
                "duration_" + str(i)
                for i in range(1, coordinator.config[CONF_COUNT] + 1)
            ]
        ],
    )


class IRRINumber(CoordinatorEntity, NumberEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
