# Meteoblue Weather Integration for Home Assistant

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/ludwig/meteoblue-home-assistant?style=for-the-badge&color=brightgreen)](https://github.com/ludwig/meteoblue-home-assistant/releases)

A custom Home Assistant integration for the **Meteoblue** weather service API. Get accurate weather data including current conditions, hourly forecasts, and daily forecasts directly from one of Europe's most trusted weather services.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ludwig&repository=meteoblue-home-assistant&category=integration)

## ✨ Features

- 🌡️ **Current weather conditions** (temperature, humidity, pressure, wind, UV index)
- ⏰ **Hourly forecasts** (next 24 hours with detailed data)
- 📅 **Daily forecasts** (up to 7 days with min/max temperatures)
- 🌍 **Flexible location setup** (use HA location or specify custom coordinates)
- 🔑 **Secure API key authentication**
- 🎯 **Automatic weather condition mapping** from Meteoblue pictocodes to HA conditions
- ⚡ **Efficient data updates** with built-in error handling and rate limiting

## 🚀 Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the 3 dots (top right) → "Custom repositories"
4. Add this repository URL: `https://github.com/ludwig/meteoblue-home-assistant`
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
3. Choose a plan (free tier includes 1000+ calls/day)
4. Copy your API key

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

### Current Conditions

- 🌡️ Temperature, humidity, pressure
- 💨 Wind speed, direction, and gusts
- ☀️ UV index and visibility
- ☁️ Cloud coverage and weather condition

### Forecasts

- **Hourly**: Next 24 hours with detailed metrics
- **Daily**: Up to 7 days with min/max temperatures
- 🌧️ Precipitation amount and probability
- 💨 Wind conditions and humidity
- ☀️ UV index predictions

## 🔧 Technical Details

### API Usage

The integration uses the Meteoblue Forecast API:

- **Packages**: `basic-1h` (hourly) + `basic-day` (daily)
- **Updates**: Every 10 minutes (configurable)
- **Rate Limits**: Respects API limits (500 calls/min, daily quota)

### Weather Condition Mapping

Meteoblue pictocodes are automatically mapped to Home Assistant conditions:

- ☀️ Clear/Sunny → `sunny`
- ⛅ Partly Cloudy → `partlycloudy`
- ☁️ Cloudy/Overcast → `cloudy`
- 🌫️ Fog → `fog`
- 🌧️ Rain (light/heavy) → `rainy` / `pouring`
- ❄️ Snow → `snowy`
- 🌨️ Mixed precipitation → `snowy-rainy`
- ⛈️ Thunderstorms → `lightning-rainy`

## 🐛 Troubleshooting

### Common Issues

| Problem                    | Solution                                                |
| -------------------------- | ------------------------------------------------------- |
| ❌ **Invalid API Key**     | Verify your Meteoblue API key is correct and active     |
| 🌐 **Cannot Connect**      | Check internet connection and API endpoint availability |
| ⏱️ **Rate Limit Exceeded** | Reduce polling frequency or check API usage limits      |
| 📍 **Wrong Location Data** | Verify latitude/longitude coordinates are correct       |

### Debug Logging

Enable detailed logging by adding this to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.meteoblue: debug
```

## 📊 API Limits

**Free Tier Limits:**

- 🎯 1,000+ calls per day
- ⚡ 500 calls per minute
- 📈 Monitor usage in [Meteoblue Dashboard](https://www.meteoblue.com/)

## 🤝 Contributing

Found a bug or have a feature request?

- 🐛 [Report Issues](https://github.com/ludwig/meteoblue-home-assistant/issues)
- 💡 [Request Features](https://github.com/ludwig/meteoblue-home-assistant/discussions)
- 🔧 [Submit Pull Requests](https://github.com/ludwig/meteoblue-home-assistant/pulls)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>🌤️ Enjoying accurate weather data? Give this repo a ⭐!</strong>
</p>
