# ☁️ Cloud Oracle — Weather Forecast App
## A simple machine learning–powered weather forecasting app built with Python.

# 🌦 Overview
#### Cloud Oracle predicts today’s high and low temperatures using machine learning. The project demonstrates how to build a complete ML pipeline from data collection to training and prediction all in a single, modular Python project.

# Limitations
#### This project is intended for research and learning purposes only. Forecasts may deviate by approximately 3–4% from real-world data

# ⚙️ Features
    🌐 Crawler — collects historical and current weather data from website.

    🧠 Model Trainer — builds and trains an ML model using the crawled dataset.

    🔮 Forecaster — predicts today’s high and low temperatures.

    📊 Visualization Support — Jupyter notebooks for exploratory data analysis and visualization.

# 🚀 Getting Started
## Prerequisites
### Install all dependencies using the following command
```bash
pip install -r requirements.txt
```
## 📦 Installation & Usage
### 1. Clone the repository
```bash
    git clone https://github.com/jenovax86/Cloud-Oracle.git
    cd Cloud-oracle
```
### 2. Create database table:
```bash
    python -m database
```
### 3. Run the crawler (collects weather data)
```bash
 python -m crawler
```
### 4. Train the model
```bash
 python -m model
```
### 5. Generate predictions
```bash
 python -m example
```

## Visualized Analysis
### To explore the data and model performance visually, run
```bash
    cd notebook
    jupyter lab
```
or
```bash
    jupyter notebook
```
