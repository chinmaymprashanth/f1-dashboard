
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏁 Formula 1 — Race Results Explorer")

# Load data
df = pd.read_csv("results_full.csv", parse_dates=["date"])

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎯 Filter by Race")

# 1. Year dropdown
years = df["year"].sort_values().unique()
selected_year = st.sidebar.selectbox("Select Year", years)

# 2. Race name dropdown based on selected year
filtered_year_df = df[df["year"] == selected_year]
race_names = filtered_year_df["race_name"].unique()
selected_race = st.sidebar.selectbox("Select Race", race_names)

# --- FILTERED DATA ---
filtered_df = df[
    (df["year"] == selected_year) &
    (df["race_name"] == selected_race)
].sort_values("position_num")

# --- DISPLAY ---
st.subheader(f"📊 Results: {selected_race} ({selected_year})")
st.dataframe(filtered_df[[
    "position_num", "forename", "surname", "constructor_name",
    "grid", "points", "laps", "fastestLapTime"
]].rename(columns={
    "position_num": "Position",
    "forename": "First Name",
    "surname": "Last Name",
    "constructor_name": "Team",
    "grid": "Grid Start",
    "points": "Points",
    "laps": "Laps",
    "fastestLapTime": "Fastest Lap"
}), use_container_width=True)
st.subheader("⬇️ Download Race Results")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"F1_{selected_year}_{selected_race}.csv",
    mime="text/csv",
)


st.subheader("🏆 Podium — Top 3 Drivers")

# Keep only top 3
podium_df = filtered_df.head(3)
# Rearrange for podium layout:
podium_df_sorted = podium_df.sort_values("position_num")

# Assign custom X positions to look like podium:
podium_df_sorted["podium_x"] = [2, 1, 3]

# Define your color mapping
color_map = {
    "Red Bull": "#1E5BC6",
    "Ferrari": "#C00000",
    "Mercedes": "#00D2BE",
    "McLaren": "#FF8700",
    "Williams": "#005AFF",
    "Alpine F1 Team": "#2293D1",
    "Aston Martin": "#006F62",
    "Alfa Romeo": "#900000",
    "Haas F1 Team": "#B6BABD",
    "AlphaTauri": "#2B4562"
}

# Create figure:
fig = go.Figure()

# Add bars:
for _, row in podium_df_sorted.iterrows():
    fig.add_trace(go.Bar(
        x=[row["podium_x"]],
        y=[row["points"]],
        name=row["surname"],
        text=f"{row['surname']}<br>{int(row['points'])} pts",
        textposition="outside",
        marker_color=color_map.get(row["constructor_name"], "gray"),
        hovertext=f"{row['surname']}<br>{row['constructor_name']}<br>{row['points']} pts",
        hoverinfo="text"
    ))

# Layout styling
fig.update_layout(
    title=f"🏆 Podium — {selected_race} {selected_year}",
    showlegend=False,
    height=500,
    xaxis=dict(
        tickvals=[1, 2, 3],
        ticktext=["2nd", "1st", "3rd"],
        title="Podium Position"
    ),
    yaxis=dict(
        title="Points",
        showgrid=False
    ),
    bargap=0,
    margin=dict(l=40, r=40, t=80, b=40)
)
fig.update_yaxes(range=[0, 26 * 1.2])

st.plotly_chart(fig, use_container_width=True)



st.subheader("🚥 Positions Gained / Lost")

# Compute positions gained/lost
filtered_df["positions_gained"] = filtered_df["grid"] - filtered_df["position_num"]

# Sort drivers by gained/lost for better visuals
sorted_df = filtered_df.sort_values("positions_gained", ascending=False)

fig_pos_gain = px.bar(
    sorted_df,
    x="positions_gained",
    y="surname",
    color="constructor_name",
    text="positions_gained",
    orientation="h",
    title=f"Positions Gained/Lost — {selected_race} {selected_year}",
    labels={
        "positions_gained": "Positions Gained (+) or Lost (-)",
        "surname": "Driver",
        "constructor_name": "Team"
    },
    height=500
)

st.plotly_chart(fig_pos_gain, use_container_width=True)


st.subheader("⏱️ Lap Times Analysis")

# Filter drivers available in the race
drivers_in_race = filtered_df["surname"].unique()

selected_driver = st.selectbox(
    "Select Driver to Plot Lap Times",
    drivers_in_race
)

# Load lap_times.csv only once
@st.cache_data
def load_lap_times():
    df_laps = pd.read_csv("lap_times_full.csv")
    return df_laps

lap_times_df = load_lap_times()

# Filter lap times for selected race and driver
driver_laps = lap_times_df[
    (lap_times_df["raceId"] == filtered_df["raceId"].iloc[0]) &
    (lap_times_df["driverId"] == filtered_df[filtered_df["surname"] == selected_driver]["driverId"].iloc[0])
]
driver_laps["minutes"] = driver_laps["milliseconds"] / 60000


# Check if data exists
if not driver_laps.empty:
    fig_laps = px.line(
        driver_laps,
        x="lap",
        y="minutes",
        title=f"Lap Times for {selected_driver} - {selected_race} {selected_year}",
        labels={"lap": "Lap Number", "minutes": "Lap Time (minutes)"}
    )
    st.plotly_chart(fig_laps, use_container_width=True)
else:
    st.info("No lap times found for this driver in this race.")

    st.subheader("🛠️ Pit Stop Details for Selected Driver")

# Get raceId from filtered_df
race_id = filtered_df["raceId"].iloc[0]

# Get driverId from filtered_df
driver_id = filtered_df[filtered_df["surname"] == selected_driver]["driverId"].iloc[0]

    # Load pit_stops.csv once
@st.cache_data
def load_pit_stops():
    return pd.read_csv("pit_stops_full.csv")

pit_stops_df = load_pit_stops()

# Filter for this race and driver
pit_data = pit_stops_df[
(pit_stops_df["raceId"] == race_id) &
(pit_stops_df["driverId"] == driver_id)
]

if not pit_data.empty:
# Show relevant columns
    st.dataframe(
    pit_data[["lap", "stop", "duration"]],
    use_container_width=True
)
else:
    st.info(f"No pit stops for {selected_driver} in this race.")

st.subheader("👥 Driver Comparison")

# Get list of drivers in this race
drivers_list = filtered_df["surname"].unique()

# Let user pick two drivers
driver1 = st.selectbox("Select Driver 1", drivers_list, key="drv1")
driver2 = st.selectbox("Select Driver 2", drivers_list, key="drv2")

if driver1 != driver2:
    # Get their rows
    d1_row = filtered_df[filtered_df["surname"] == driver1].iloc[0]
    d2_row = filtered_df[filtered_df["surname"] == driver2].iloc[0]

    # Create a comparison DataFrame
    comparison_df = pd.DataFrame({
        "Metric": [
            "Grid Start",
            "Finish Position",
            "Positions Gained/Lost",
            "Laps Completed",
            "Points Scored",
            "Fastest Lap Time"
        ],
        driver1: [
            d1_row["grid"],
            d1_row["position_num"],
            d1_row["grid"] - d1_row["position_num"] if pd.notnull(d1_row["position_num"]) else "N/A",
            d1_row["laps"],
            d1_row["points"],
            d1_row["fastestLapTime"]
        ],
        driver2: [
            d2_row["grid"],
            d2_row["position_num"],
            d2_row["grid"] - d2_row["position_num"] if pd.notnull(d2_row["position_num"]) else "N/A",
            d2_row["laps"],
            d2_row["points"],
            d2_row["fastestLapTime"]
        ]
    })

    st.dataframe(comparison_df, use_container_width=True)

else:
    st.info("Please select two different drivers to compare.")
st.header("🏆 Championship Standings")

# Driver standings till selected race
selected_date = filtered_df["date"].iloc[0]

season_upto_selected = df[
    (df["year"] == selected_year) &
    (df["date"] <= selected_date)
]

driver_standings_partial = season_upto_selected.groupby(
    ["driverId", "forename", "surname"]
)["points"].sum().reset_index()

driver_standings_partial = driver_standings_partial.sort_values(
    "points", ascending=False
)

driver_standings_partial = driver_standings_partial.rename(columns={
    "forename": "First Name",
    "surname": "Last Name",
    "points": "Total Points"
})

st.subheader(f"🏎️ Driver Standings till {selected_race} ({selected_year})")
st.dataframe(driver_standings_partial, use_container_width=True)


# Total driver points in the selected year
driver_standings = (
    df[df["year"] == selected_year]
    .groupby(["driverId", "forename", "surname"])
    .agg(total_points=("points", "sum"))
    .reset_index()
    .sort_values("total_points", ascending=True)
)

st.subheader("Driver Standings")

fig_driver = px.bar(
    driver_standings,
    x="total_points",
    y=driver_standings["forename"] + " " + driver_standings["surname"],
    orientation="h",
    title=f"Total Driver Points - {selected_year}",
    labels={"total_points": "Total Points", "y": "Driver"},
    height=600
)

st.plotly_chart(fig_driver, use_container_width=True)

# --- Constructor Standings up to selected race ---

# Get selected race date
selected_date = filtered_df["date"].iloc[0]

# All races until selected race
season_upto_selected = df[
    (df["year"] == selected_year) &
    (df["date"] <= selected_date)
]

# Group points by constructor
constructor_standings_partial = season_upto_selected.groupby(
    ["constructorId", "constructor_name"]
)["points"].sum().reset_index()

# Sort descending
constructor_standings_partial = constructor_standings_partial.sort_values(
    "points", ascending=False
)

# Rename for display
constructor_standings_partial = constructor_standings_partial.rename(columns={
    "constructor_name": "Team",
    "points": "Total Points"
})

st.subheader(f"🏎️ Constructor Standings till {selected_race} ({selected_year})")
st.dataframe(constructor_standings_partial, use_container_width=True)


# CONSTRUCTOR standings for whole season
constructor_standings_total = df[
    df["year"] == selected_year
].groupby(["constructorId", "constructor_name"])["points"].sum().reset_index()

constructor_standings_total = constructor_standings_total.rename(
    columns={"constructor_name": "Team"}
).sort_values("points", ascending=False)

fig_const_total = px.bar(
    constructor_standings_total,
    x="Team",
    y="points",
    text="points",
    title=f"Constructor Championship Standings - {selected_year}",
    labels={"Team": "Constructor", "points": "Total Points"},
    color="points",
    height=600
)

fig_const_total.update_traces(textposition='outside')
fig_const_total.update_layout(yaxis_title="Total Points")

st.subheader(f"🏆 Constructor Championship Standings - {selected_year}")
st.plotly_chart(fig_const_total, use_container_width=False)
