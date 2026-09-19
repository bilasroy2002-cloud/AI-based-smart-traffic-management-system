# AI-based-smart-traffic-management-system
This project demonstrates an AI-based traffic control system that:

- collects live traffic sensor data
- predicts congestion severity using a simple scoring model
- optimizes traffic signal timing for busy directions
- reduces travel delay, fuel use, and emissions

## Features

- Real-time congestion prediction
- Adaptive signal timing optimization
- Demand-based green-time allocation
- Simulation-friendly CLI interface

## Project Structure

- `traffic_system.py` – prediction and optimization logic
- `app.py` – command-line simulator entry point
- `tests/test_traffic_system.py` – validation tests

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows PowerShell
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the traffic simulator:

   ```bash
   python app.py --vehicle-count 800 --avg-speed 22 --occupancy 75 --queue-length 160 --weather 0.8 --time-of-day evening_peak
   ```

4. Run tests:

   ```bash
   pytest -q
   ```
## LINK TO THE SITE
   http://127.0.0.1:5000


## How to upload this project to GitHub

1. Initialize a Git repository:

   ```bash
   git init
   ```

2. Add the files:

   ```bash
   git add .
   ```

3. Commit the code:

   ```bash
   git commit -m "Initial AI traffic management system"
   ```

4. Create a repository on GitHub and copy the remote URL.

5. Connect the repository:

   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

6. Push the project:

   ```bash
   git push -u origin main
   ```

If you prefer GitHub CLI:

```bash
gh repo create YOUR_REPO_NAME --public --source=. --remote=origin --push
```

## Use cases

This system can support:

- smart city traffic management
- emergency vehicle prioritization
- adaptive traffic control for peak-hour conditions
- city-level carbon reduction planning

## Future improvements

- connect to live traffic APIs (Google Maps, TomTom, HERE)
- use machine learning models for better congestion forecasting
- visualize the signal plan in a dashboard
- integrate with IoT traffic sensors
