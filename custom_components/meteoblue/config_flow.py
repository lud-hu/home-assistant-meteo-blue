"""Config flow for Meteoblue integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    API_URL_BASE,
    CONF_API_KEY,
    CONF_ELEVATION,
    DEFAULT_NAME,
    DOMAIN,
    ENABLE_DEBUG_LOGGING,
)

_LOGGER = logging.getLogger(__name__)

# Disable debug logging if flag is False
if not ENABLE_DEBUG_LOGGING:
    _LOGGER.setLevel(logging.INFO)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_LATITUDE): cv.latitude,
        vol.Optional(CONF_LONGITUDE): cv.longitude,
        vol.Optional(CONF_ELEVATION): cv.positive_int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    _LOGGER.debug("Validating user input for Meteoblue setup")
    _LOGGER.debug(
        "Input data: %s",
        {k: "***" if k == CONF_API_KEY else v for k, v in data.items()},
    )

    session = async_get_clientsession(hass)

    # Use provided coordinates or fall back to Home Assistant defaults
    latitude = data.get(CONF_LATITUDE, hass.config.latitude)
    longitude = data.get(CONF_LONGITUDE, hass.config.longitude)

    _LOGGER.debug("Using coordinates: lat=%s, lon=%s", latitude, longitude)

    if latitude is None or longitude is None:
        _LOGGER.error("No valid coordinates provided or configured in Home Assistant")
        raise ValueError("Latitude and longitude must be provided")  # Test API call
    url = f"{API_URL_BASE}/basic-day"
    params = {
        "lat": latitude,
        "lon": longitude,
        "apikey": data[CONF_API_KEY],
        "forecast_days": 1,
        "format": "json",
    }

    if CONF_ELEVATION in data:
        params["asl"] = data[CONF_ELEVATION]

    _LOGGER.debug("Testing API connection to: %s", url)
    safe_params = {k: "***" if k == "apikey" else v for k, v in params.items()}
    _LOGGER.debug("Test request parameters: %s", safe_params)

    try:
        async with asyncio.timeout(30):
            async with session.get(url, params=params) as response:
                _LOGGER.debug("Test API response status: %s", response.status)

                if response.status == 401:
                    _LOGGER.error("API key validation failed")
                    raise InvalidAuth("Invalid API key")
                elif response.status == 429:
                    _LOGGER.error("API rate limit exceeded during validation")
                    raise CannotConnect("API rate limit exceeded")
                elif response.status != 200:
                    _LOGGER.error(
                        "API validation failed with status: %s", response.status
                    )
                    raise CannotConnect(f"API returned status {response.status}")

                result = await response.json()
                _LOGGER.debug("API validation successful")

                # Return location name if available
                location_name = DEFAULT_NAME
                if "metadata" in result and "name" in result["metadata"]:
                    location_name = result["metadata"]["name"]
                    _LOGGER.debug("Detected location name: %s", location_name)

                return {"title": location_name}

    except asyncio.TimeoutError as ex:
        _LOGGER.error("Timeout during API validation after 30 seconds")
        raise CannotConnect("Timeout connecting to Meteoblue API") from ex
    except aiohttp.ClientError as ex:
        _LOGGER.error("Network error during API validation: %s", ex)
        raise CannotConnect(f"Error connecting to Meteoblue API: {ex}") from ex


class MeteoblueConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Meteoblue."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        _LOGGER.debug("Config flow step_user called")
        errors: dict[str, str] = {}

        if user_input is not None:
            _LOGGER.info("Processing user input for Meteoblue config")
            try:
                info = await validate_input(self.hass, user_input)
                _LOGGER.debug("Input validation successful")
            except CannotConnect as ex:
                _LOGGER.error("Cannot connect to Meteoblue API: %s", ex)
                errors["base"] = "cannot_connect"
            except InvalidAuth as ex:
                _LOGGER.error("Invalid authentication: %s", ex)
                errors["base"] = "invalid_auth"
            except ValueError as ex:
                _LOGGER.error("Invalid location data: %s", ex)
                errors["base"] = "invalid_location"
            except Exception as ex:
                _LOGGER.error(
                    "Unexpected exception during validation: %s", ex, exc_info=True
                )
                errors["base"] = "unknown"
            else:
                # Check if already configured
                unique_id = f"{user_input[CONF_API_KEY]}-{user_input.get(CONF_LATITUDE, self.hass.config.latitude)}-{user_input.get(CONF_LONGITUDE, self.hass.config.longitude)}"
                _LOGGER.debug("Setting unique_id: %s", unique_id[:20] + "...")
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                _LOGGER.info("Creating config entry for Meteoblue: %s", info["title"])
                return self.async_create_entry(title=info["title"], data=user_input)
        else:
            _LOGGER.debug("Showing initial config form")

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
