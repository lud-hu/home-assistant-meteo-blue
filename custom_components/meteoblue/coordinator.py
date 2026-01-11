"""DataUpdateCoordinator for Meteoblue."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_URL_BASE,
    CONF_API_KEY,
    CONF_ELEVATION,
    DEFAULT_FORECAST_DAYS,
    DEFAULT_PACKAGES,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    ENABLE_DEBUG_LOGGING,
    PICTOCODE_TO_CONDITION,
)

_LOGGER = logging.getLogger(__name__)

# Disable debug logging if flag is False
if not ENABLE_DEBUG_LOGGING:
    _LOGGER.setLevel(logging.INFO)


type MeteoblueConfigEntry = ConfigEntry[MeteoblueDataUpdateCoordinator]


class MeteoblueDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Meteoblue data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        self.config_entry = config_entry
        self._api_key = config_entry.data[CONF_API_KEY]
        self._latitude = config_entry.data.get(CONF_LATITUDE, hass.config.latitude)
        self._longitude = config_entry.data.get(CONF_LONGITUDE, hass.config.longitude)
        self._elevation = config_entry.data.get(CONF_ELEVATION)
        self._session = async_get_clientsession(hass)
        self._last_request_time = None

        _LOGGER.debug(
            "Initializing coordinator with coordinates: lat=%s, lon=%s, elevation=%s",
            self._latitude,
            self._longitude,
            self._elevation,
        )
        _LOGGER.debug("API key configured: %s", bool(self._api_key))

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

        _LOGGER.info(
            "Coordinator initialized with update interval: %s seconds",
            DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Meteoblue API."""
        _LOGGER.info(
            "Update triggered for coordinates: lat=%s, lon=%s",
            self._latitude,
            self._longitude,
        )

        # Strict interval enforcement: only allow updates according to configured interval
        now = datetime.now()
        if self._last_request_time:
            time_since_last = (now - self._last_request_time).total_seconds()
            min_interval = DEFAULT_SCAN_INTERVAL * 0.95  # Allow 5% tolerance

            if time_since_last < min_interval:
                _LOGGER.debug(
                    "Interval enforcement: skipping update, only %s seconds since last request (minimum: %s)",
                    int(time_since_last),
                    int(min_interval),
                )
                if self.data:
                    return self.data
                else:
                    _LOGGER.warning(
                        "No cached data available, but enforcing update interval - will wait for next scheduled update"
                    )
                    raise UpdateFailed(
                        "Enforcing update interval, no cached data available"
                    )

        try:
            data = await self._fetch_weather_data()
            self._last_request_time = now
            _LOGGER.info("Successfully fetched weather data")
            _LOGGER.debug(
                "Data contains keys: %s", list(data.keys()) if data else "None"
            )
            return data
        except Exception as ex:
            _LOGGER.error(
                "Error communicating with Meteoblue API: %s", ex, exc_info=True
            )
            raise UpdateFailed(f"Error communicating with Meteoblue API: {ex}") from ex

    async def _fetch_weather_data(self) -> dict[str, Any]:
        """Fetch weather data from Meteoblue API."""
        url = f"{API_URL_BASE}/{DEFAULT_PACKAGES}"

        params = {
            "lat": self._latitude,
            "lon": self._longitude,
            "apikey": self._api_key,
            "format": "json",
            "forecast_days": DEFAULT_FORECAST_DAYS,
        }

        if self._elevation is not None:
            params["asl"] = self._elevation

        # Log API request (without exposing API key)
        safe_params = {k: "***" if k == "apikey" else v for k, v in params.items()}
        _LOGGER.debug("Making API request to: %s", url)
        _LOGGER.debug("Request parameters: %s", safe_params)

        try:
            async with asyncio.timeout(30):
                async with self._session.get(url, params=params) as response:
                    _LOGGER.debug("API response status: %s", response.status)
                    _LOGGER.debug("API response headers: %s", dict(response.headers))

                    if response.status == 401:
                        _LOGGER.error("API authentication failed - check API key")
                        raise UpdateFailed("Invalid API key")
                    elif response.status == 429:
                        _LOGGER.warning("API rate limit exceeded")
                        raise UpdateFailed("API rate limit exceeded")
                    elif response.status != 200:
                        _LOGGER.error(
                            "API returned unexpected status: %s", response.status
                        )
                        response_text = await response.text()
                        _LOGGER.debug("API error response: %s", response_text)
                        raise UpdateFailed(f"API returned status {response.status}")

                    data = await response.json()
                    _LOGGER.debug("Received API response with %s bytes", len(str(data)))
                    return self._process_weather_data(data)

        except asyncio.TimeoutError as ex:
            _LOGGER.error("Timeout communicating with Meteoblue API after 30 seconds")
            raise UpdateFailed("Timeout communicating with Meteoblue API") from ex
        except aiohttp.ClientError as ex:
            _LOGGER.error("Network error communicating with Meteoblue API: %s", ex)
            raise UpdateFailed(f"Error communicating with Meteoblue API: {ex}") from ex

    def _process_weather_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw API data into structured format."""
        processed_data = {
            "metadata": raw_data.get("metadata", {}),
            "units": raw_data.get("units", {}),
            "current": None,
            "daily_forecast": [],
        }

        # Process daily forecast
        if "data_day" in raw_data:
            daily_data = raw_data["data_day"]
            processed_data["daily_forecast"] = self._extract_daily_forecast(daily_data)
            # Use first day data as current conditions
            if processed_data["daily_forecast"]:
                processed_data["current"] = processed_data["daily_forecast"][0].copy()
                # Convert daily data to current format for compatibility
                if "temperature_max" in processed_data["current"]:
                    processed_data["current"]["temperature"] = processed_data[
                        "current"
                    ]["temperature_max"]
                if "temperature_min" in processed_data["current"]:
                    processed_data["current"]["temperature_low"] = processed_data[
                        "current"
                    ]["temperature_min"]

        return processed_data

    def _extract_daily_forecast(
        self, daily_data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Extract daily forecast from API data."""
        if not daily_data.get("time"):
            return []

        forecast = []
        time_list = daily_data["time"]

        for i in range(len(time_list)):
            day_data = {"time": time_list[i]}

            for key, values in daily_data.items():
                if key != "time" and values and len(values) > i:
                    day_data[key] = values[i]

            # Convert pictocode to condition
            if "pictocode" in day_data:
                day_data["condition"] = PICTOCODE_TO_CONDITION.get(
                    day_data["pictocode"], "unknown"
                )

            forecast.append(day_data)

        return forecast

    @property
    def location_name(self) -> str:
        """Return location name."""
        if self.data and "metadata" in self.data:
            return self.data["metadata"].get("name", "Unknown")
        return "Unknown"

    @property
    def current_weather(self) -> dict[str, Any] | None:
        """Return current weather data."""
        return self.data.get("current") if self.data else None

    @property
    def daily_forecast(self) -> list[dict[str, Any]]:
        """Return daily forecast data."""
        return self.data.get("daily_forecast", []) if self.data else []

    async def async_request_refresh(self) -> None:
        """Request a refresh but respect the update interval."""
        _LOGGER.debug("Manual refresh requested")

        if self._last_request_time:
            time_since_last = (datetime.now() - self._last_request_time).total_seconds()
            min_interval = DEFAULT_SCAN_INTERVAL * 0.95  # Allow 5% tolerance

            if time_since_last < min_interval:
                remaining_time = int(min_interval - time_since_last)
                _LOGGER.info(
                    "Manual refresh denied - respecting update interval. Next update in %s seconds (%s minutes)",
                    remaining_time,
                    int(remaining_time / 60),
                )
                return

        _LOGGER.info("Manual refresh allowed - sufficient time since last update")
        await super().async_request_refresh()
