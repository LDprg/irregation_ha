"""Platform for sensor integration."""

from __future__ import annotations
from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)

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
        [IRRITime(coordinator, name) for name in ["start_time"]],
    )


class IRRITime(CoordinatorEntity, TimeEntity, RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Restore last state."""
        await super().async_added_to_hass()
        if (
            last_state := await self.async_get_last_state()
        ) is not None and last_state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
            irri.LOGGER.warn(f"RESTORE TIME: {last_state}")
            self._attr_native_value = time.fromisoformat(last_state.state)

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()
