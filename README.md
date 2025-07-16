# f1-dashboard

# 🏁 Formula 1 Race Results Dashboard

An interactive **F1 race analytics dashboard** built with **Streamlit**, **Pandas**, and **Plotly** — visualize race results, lap times, pit stop strategies, and championship standings for any Formula 1 season.

> 🔧 Built as a personal data project to explore real-world motorsport data and deploy a live analytics tool online.

---

## 🚀 Live Demo

👉 [View the App](https://f1-dashboard.streamlit.app) — hosted on **Streamlit Community Cloud**

---

## 📸 Features

### 🎯 Filter by Year and Race
- Select a race season (e.g. 2011) and a specific Grand Prix (e.g. Australian GP)
- See full race results with driver, team, grid start, points, laps, and fastest lap

### 🏆 Podium Visualizer
- Custom podium-style bar chart showing the **top 3 finishers**
- Styled bars for 1st, 2nd, and 3rd with driver names and team colors

### ⏱️ Lap Time Analysis
- Pick a driver to see their **lap-by-lap performance**
- Interactive line plot to analyze consistency, pace drop, or safety car effects

### 🛠️ Pit Stop Table
- Shows **when** a selected driver made pit stops and for how long

### 🔄 Start vs Finish Comparison
- See how many positions each driver gained or lost during the race

### ⚔️ Driver vs Driver Comparison
- Compare two drivers' stats side by side: laps, points, fastest lap, pit stops, etc.

### 🏁 Season Standings
- **Championship table** for both drivers and constructors
- Compare total points and view standings up to a selected race

### 📥 Download Results
- One-click download of filtered race data as a CSV

---

## 📂 Dataset

This app uses cleaned and pre-joined F1 datasets based on public sources such as:
- [Ergast API](https://ergast.com/mrd/)
- [Kaggle F1 datasets](https://www.kaggle.com/c/gstore/data)

### Files Used:
| File Name           | Description                             |
|---------------------|-----------------------------------------|
| `results_full.csv`  | Joined data of races, drivers, results  |
| `lap_times_full.csv`| Lap-by-lap timing data per driver       |
| `pit_stops_full.csv`| Pit stop lap, time, and duration        |
| `drivers.csv`       | Driver names, DOB, nationality, etc.    |
| `constructors.csv`  | Constructor/team information            |
| `races.csv`         | Race calendar with raceId and year      |

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — for UI and deployment
- [Pandas](https://pandas.pydata.org/) — for data processing
- [Plotly](https://plotly.com/python/) — for interactive visualizations
- Python 3.11+

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/f1-dashboard.git
cd f1-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run f1_app.py
