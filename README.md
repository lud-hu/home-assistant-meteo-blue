# Meteoblue Weather Integration for Home Assistant

A custom Home Assistant integration for the **Meteoblue** weather service API. Get accurate weather forecasts directly from one of Europe's most trusted weather services.

Note: The integration is optimized for usage with [meteoblue's free API](https://content.meteoblue.com/en/business-solutions/weather-apis) tier, therefore only daily forecasts (not hourly) are polled every 6 hours. This allows to stay within the limit of 10.000.000 credits per year.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=lud-hu&repository=home-assistant-meteo-blue&category=integration)

## ✨ Features

- 📅 **Daily forecasts** (up to 7 days with min/max temperatures)
- 🌍 **Flexible location setup** (use HA location or specify custom coordinates)
- 🔑 **API key authentication** (use your personal meteoblue API key)
- 🎯 **Automatic weather condition mapping** from Meteoblue pictocodes to HA conditions
- ⚡ **Efficient data updates** every 6 hours to stay within free tier of API

## 🚀 Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the 3 dots (top right) → "Custom repositories"
4. Add this repository URL: `https://github.com/lud-hu/home-assistant-meteo-blue`
5. Category: "Integration"
6. Click "Add", then install "Meteoblue Weather"
7. **Restart Home Assistant**

### Manual Installation

1. Copy the `custom_components/meteoblue` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## ⚙️ Configuration

### Prerequisites

You need a **Meteoblue API key** to use this integration.

📋 **Get your free API key:**

1. Visit [Meteoblue Developer Portal](https://content.meteoblue.com/en/business-solutions/weather-apis)
2. Sign up for a free account
3. Copy your API key

### Setup

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "**Meteoblue**"
3. Enter your configuration:
   - **🔑 API Key**: Your Meteoblue API key _(required)_
   - **📍 Name**: Custom name for this weather station _(optional)_
   - **🌍 Latitude**: Location latitude _(optional - uses HA location)_
   - **🌍 Longitude**: Location longitude _(optional - uses HA location)_
   - **🏔️ Elevation**: Location elevation in meters _(optional - auto-detected)_

## 🌦️ Weather Data

- **Daily**: Up to 7 days with min/max temperatures
- 🌧️ Precipitation amount and probability
- 💨 Wind conditions and humidity
- ☀️ UV index predictions
- and more, see [API docs](https://docs.meteoblue.com/en/weather-apis/forecast-api/overview)

## 🔧 Technical Details

### API Usage

The integration uses the Meteoblue Forecast API:

- **Packages**: `basic-day` (daily)
- **Updates**: Every 6 hours (optimized for API quota)

### Weather Condition Mapping

Meteoblue pictocodes are automatically mapped to Home Assistant conditions:
https://content.meteoblue.com/en/research-education/specifications/standards/symbols-and-pictograms

## 🐛 Troubleshooting

### Debug Logging

The integration includes comprehensive debug logging that can be easily controlled.

**Enable/Disable Debug Logging:**

1. **Via Code (Development):** Edit `custom_components/meteoblue/const.py`:

   ```python
   # Set to True to enable debug logs, False to disable them
   ENABLE_DEBUG_LOGGING = True
   ```

   When `ENABLE_DEBUG_LOGGING = False`, the logger level is set to INFO, effectively disabling all debug messages while keeping info, warning, and error messages.

2. **Via Home Assistant Configuration:** Add to `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.meteoblue: debug # or info, warning, error
   ```

**What Gets Logged:**

- API requests and responses (with masked API keys)
- Data processing steps and results
- Entity state changes and updates
- Error conditions with full context

## 🤝 Contributing

Found a bug or have a feature request?

- 🐛 [Report Issues](https://github.com/lud-hu/home-assistant-meteo-blue/issues)
- 💡 [Request Features](https://github.com/lud-hu/home-assistant-meteo-blue/issues)
- 🔧 [Submit Pull Requests](https://github.com/lud-hu/home-assistant-meteo-blue/pulls)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>🌤️ Enjoying accurate weather data? Give this repo a ⭐!</strong>
</p>
