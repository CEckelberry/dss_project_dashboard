# Data Science and Society Dashboard: Greenhouse Gas Emissions for the Benelux Region and Solar as our Savior

## Overview

The aim with this dashboard is to provide the governments of the Benelux with information on various aspects of energy consumption and solar energy production. The dashboard will encompass an overview of energy consumption across industries, the current state of solar energy generated in the Benelux, and how solar energy can help them with their nationally determined contributions, that each country sets to achieve the Paris Agreement goals.

## Setup

The dashboard is containerized using Docker. Follow these steps to set it up:

### Prerequisites

- Docker installed and running on your machine.

### Installation

1. Clone this repository.
2. run the following command: `docker-compose up --build`
3. Wait for the PostgreSQL database to initialize, and the uploader script to insert data. Look for specific confirmation lines in the terminal (shown below).
   ![uploader has finished](image.png)

## Using the Dashboard

- Access the Dashboard at: http://localhost:8501/
- The Dashboard caches queries for improved performance. Switching between panels should not always trigger a re-run of queries. Sometimes you might need to refresh if your screen isn't showing the page icon's.
