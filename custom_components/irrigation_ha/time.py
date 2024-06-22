"""Platform for sensor integration."""

from __future__ import annotations
import dataclasses
from datetime import time
from typing import Any, Self

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import ExtraStoredData, RestoreEntity

from . import const as irri
from .coordinator import IRRICoordinator


@dataclasses.dataclass
class TimeExtraStoredData(ExtraStoredData):
    """Object to hold extra stored data."""

    native_value: float | None

    def as_dict(self) -> dict[str, Any]:
        """Return a dict representation of the number data."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, restored: dict[str, Any]) -> Self | None:
        """Initialize a stored number state from a dict."""
        try:
            return cls(
                restored["native_value"],
            )
        except KeyError:
            return None


class RestoreTime(TimeEntity, RestoreEntity):
    """Mixin class for restoring previous number state."""

    @property
    def extra_restore_state_data(self) -> TimeExtraStoredData:
        """Return number specific state data to be restored."""
        return TimeExtraStoredData(
            self.native_value,
        )

    async def async_get_last_number_data(self) -> TimeExtraStoredData | None:
        """Restore native_*."""
        if (restored_last_extra_data := await self.async_get_last_extra_data()) is None:
            return None
        return TimeExtraStoredData.from_dict(restored_last_extra_data.as_dict())


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


class IRRITime(CoordinatorEntity, TimeEntity, RestoreTime):
    """Representation of a Sensor."""

    def __init__(self, coordinator, uid):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

        self._attr_name = uid
        self._attr_unique_id = uid

        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if (last_number_data is not None) and (
            last_number_data.native_value is not None
        ):
            await self.async_set_native_value(last_number_data.native_value)

    async def async_set_value(self, value: time) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()
