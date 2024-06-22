"Coordinator file"

from __future__ import annotations

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import Event, EventStateChangedData, callback
from homeassistant.const import CONF_ENTITY_ID
from . import const as irri


class IRRICoordinator(DataUpdateCoordinator):
    """Irrigation coordinator."""

    def __init__(self, hass, config):
        """Initialize the coordinator"""
        super().__init__(
            hass,
            irri.LOGGER,
            name=irri.DOMAIN,
        )
        self.hass = hass
        self.config = config
        self.data = {}

        async_track_state_change_event(
            self.hass,
            self.config[CONF_ENTITY_ID],
            self.async_state_changed_listener,
        )

    @callback
    def async_state_changed_listener(
        self,
        event: Event[EventStateChangedData] | None = None,
    ) -> None:
        irri.LOGGER.warn(f"RECEIVED EVENT: {event}")

        self.data[event.data["entity_id"]] = event.data["new_state"].state
        self.async_set_updated_data(self.data)
