# Cloud-Oracle 🌤️

## A Python-based weather forecaster powered by MySQL and machine learning

### Cloud-Oracle predicts the lowest and highest temperatures for 2025 using historical weather data crawled from AccuWeather.
The data is stored in MySQL, retrieved for preprocessing, and then used to train an AI/ML model for forecasting.
Results are visualized with plots to make predictions easier to interpret.

## Features

  -🌐 Crawls weather data from AccuWeather

  -💾 Stores and retrieves data from MySQL

  -🧹 Cleans and processes datasets before training

  -🤖 Trains an AI model to forecast 2025 min/max temps

  -📊 Generates plots of predictions for better visualization

# Getting Started
## Prerequisites
  -Python 3.8+
  -MySQL server (local or remote)
  -Python packages (see below)
### install dependencies:
```bash
pip install -r requirements.txt
```
### Sample requirements.txt:
```
mysql-connector-python
pandas
numpy
scikit-learn
matplotlib
datetime
selenium
calender
time
os
```
# Database Setup
  -Create a MySQL database (e.g. cloud_oracle).
  -Import crawled weather data into a table (e.g. weather_data).
  -Update connection credentials in your Python scripts (host, user, password, database).

# Usage
1. Crawl data & insert into MySQL
```bash
python core/data_collector.py
```
2. Train model & plot predictions
```bash
python core/weather_forecast_model
```
# Expected Output:
  -A plot that shows the high and low temperatures in all days of the months

# Limitations
  -Predictions are experimental — based only on crawled AccuWeather data
  -Not a substitute for official meteorological forecasts
  -Intended for educational and research purposes
