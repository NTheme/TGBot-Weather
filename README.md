# **TGBot Weather**

This is a simple Telegram bot for getting weather forecast with API support developed as a MIPT Python project.

## PERMANENTLY working bot
You can open Telegram of [NThemeWeather Bot](https://t.me/n_theme_weather_bot) and check functionality at any time.

## How to build and run local copy manually
_Here is an instruction if you want to run your own copy of **WeatherBot**_.

0. Clone the repo and go to project folder:
  ```sh
  git clone https://github.com/NTheme/TGBot-Weather.git
  cd TGBot-Weather
  ```

### Using **Docker**
Use these following steps if you have a **Docker** system installed.  
_Required docker version >= 23_

1. Build docker container by executing the following command:
  ```sh
  docker build -t weather-bot .
  ```

2. Fill TG_TOKEN and WEATHER_TOKEN and then run docker container in the background by following command:
  ```sh
  docker run -d -e TG_TOKEN=... -e WEATHER_TOKEN=... ntheme/weather-bot
  ```

### Run locally
Use this instruction if you want to just run **WeatherBot**.  
_Required python version >= 3.8_

1. Create and launch python virtual environment:
  ```sh
  python3 -m venv venv
  source  ./venv/bin/activate
  ```

2. Fill your private API Tokens of Telegram and OpenWeatherMap at _service.py_ by replacing existing value.

3. Install requirement libraries:
  ```sh
  pip3 install -r requirements.txt
  ```

4. Launch bot main file:
  ```sh
  python3 ./bot.py
  ```
  **WeatherBot** will be working in the background. Congratulations!

## Usage
Very easy and user-friendly! Check ot out by calling _bot help_.

----------------------------

### ***By NThemeDEV***
