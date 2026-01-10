"""The Meteoblue integration."""

from __future__ import annotations

import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, ENABLE_DEBUG_LOGGING
from .coordinator import MeteoblueConfigEntry, MeteoblueDataUpdateCoordinator

PLATFORMS = [Platform.WEATHER]

_LOGGER = logging.getLogger(__name__)

# Disable debug logging if flag is False
if not ENABLE_DEBUG_LOGGING:
    _LOGGER.setLevel(logging.INFO)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: MeteoblueConfigEntry
) -> bool:
    """Set up Meteoblue as config entry."""
    _LOGGER.info("Setting up Meteoblue integration for entry %s", config_entry.entry_id)
    _LOGGER.debug(
        "Config entry data: %s",
        {k: "***" if k == "api_key" else v for k, v in config_entry.data.items()},
    )

    coordinator = MeteoblueDataUpdateCoordinator(hass, config_entry)
    _LOGGER.debug("Created coordinator for %s", coordinator.location_name)

    try:
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("Initial data fetch completed successfully")
    except Exception as ex:
        _LOGGER.error("Failed to fetch initial data: %s", ex)
        raise

    config_entry.runtime_data = coordinator
    _LOGGER.debug("Coordinator assigned to runtime_data")

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    _LOGGER.info("Meteoblue integration setup completed successfully")

    return True


async def async_unload_entry(
    hass: HomeAssistant, config_entry: MeteoblueConfigEntry
) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Meteoblue integration for entry %s", config_entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    if unload_ok:
        _LOGGER.info("Meteoblue integration unloaded successfully")
    else:
        _LOGGER.error("Failed to unload Meteoblue integration")

    return unload_ok
