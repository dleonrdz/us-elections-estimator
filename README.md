# US Elections Tracker

Welcome to the US Elections Tracker! This project is a group assignment for our Natural Language Processing (NLP) course, where we applied our knowledge to a relevant and impactful use case – the US elections. Given that this is an election year, we chose this topic due to its significance and the global impact of US elections.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Project Structure](#project-structure)

## Overview

The US Elections Tracker is an interactive web application built with Streamlit that visualizes political sentiment and electoral vote distribution across different states in the US. By analyzing tweets, we estimate the sentiment towards each party and compare it with official polls. This tool provides valuable insights into the political landscape and social media influence.

## Features

- **GeoPreferences**: Visualize the distribution of electoral votes across different states, including detailed insights into the Key States Battle.
- **Who's Winning?**: Compare the overall electoral votes each party has according to our sentiment estimation versus the official polls.
- **Tweets Wars**: Track the engagement metrics over time to see which party generates more buzz on social media.
- **Tweet-o-Meter**: Analyze the political inclination of your custom tweet and see how it aligns with current sentiment.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**
```sh
git clone https://github.com/your-repo/us-elections-tracker.git
cd us-elections-tracker
 ```
2. **Install Poetry:**
```sh
pip install poetry
```
3. **Install Dependencies:**
```sh
poetry install
```
3. **Activate the virtual environment:**
```sh
poetry shell
```
## Usage

To run the Streamlit app, execute the following command within the activated virtual environment:
```sh
streamlit run streamlit_app/app.py
```
## Methodology

Our estimations are derived from a fine-tuned version of DistilBERT, applied to Twitter (now X) data focusing on political tweets. The model analyzes the sentiment of each tweet and categorizes support based on the political figure or party the tweet references.

### Sections Explained

- **GeoPreferences:** This section visualizes the distribution of electoral votes across different states, highlighting key battleground states.
- **Who's Winning?:** Provides a comparative view of the overall electoral votes each party has based on our sentiment analysis versus the official polls.
- **Tweets Wars:** Displays engagement metrics over time to show which party is generating more social media buzz.
- **Tweet-o-Meter:** Allows users to input custom tweets to analyze their political inclination and see how they align with current sentiment trends.
