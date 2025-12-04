# energy_dashboard.py
# Campus Energy Monitoring Dashboard
# Author: Kartavya Gautam

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ==============================
# BASIC PATH SETTINGS
# ==============================

DATA_FOLDER = Path("data")
EXPORT_FOLDER = Path("output")
EXPORT_FOLDER.mkdir(exist_ok=True)


# ==============================
# OBJECT-ORIENTED STRUCTURES
# ==============================

class Reading:
    """A simple container for one meter entry."""
    def __init__(self, time_stamp, energy_value):
        self.time_stamp = time_stamp
        self.energy_value = energy_value


class CampusBuilding:
    """Represents each building and all its meter readings."""
    def __init__(self, building_name):
        self.name = building_name
        self.readings = []

    def add_entry(self, reading_obj):
        self.readings.append(reading_obj)

    def total_usage(self):
        return sum(r.energy_value for r in self.readings)

    def as_dataframe(self):
        """Convert readings into a DataFrame for easy work."""
        return pd.DataFrame({
            "timestamp": [r.time_stamp for r in self.readings],
            "kwh": [r.energy_value for r in self.readings],
            "building": self.name
        })

    def quick_report(self):
        """Generate a human-readable summary for one building."""
        total = self.total_usage()
        count = len(self.readings)
        avg = total / count if count > 0 else 0

        return (
            f"Building: {self.name}\n"
            f"Total kWh Used: {total:.2f}\n"
            f"Average per Reading: {avg:.2f}\n"
            f"Entries Recorded: {count}"
        )


class CampusEnergyManager:
    """Keeps track of all buildings and connects the OOP side with DataFrames."""
    def __init__(self):
        self.registry = {}  # building_name -> CampusBuilding

    def get_building(self, name):
        if name not in self.registry:
            self.registry[name] = CampusBuilding(name)
        return self.registry[name]

    def populate_from_df(self, data: pd.DataFrame):
        for _, row in data.iterrows():
            b = self.get_building(row["building"])
            b.add_entry(Reading(row["timestamp"], row["kwh"]))

    def generate_summary_table(self):
        """Return summary df for all buildings."""
        records = []
        for name, b_obj in self.registry.items():
            df_temp = b_obj.as_dataframe()
            records.append({
                "building": name,
                "total_kwh": df_temp["kwh"].sum(),
                "mean_kwh": df_temp["kwh"].mean(),
                "min_kwh": df_temp["kwh"].min(),
                "max_kwh": df_temp["kwh"].max(),
            })
        return pd.DataFrame(records)


# ==============================
# DATA LOADING + CLEANUP
# ==============================

def read_energy_data():
    """Reads all CSVs inside data/ folder, checks for issues, merges them."""
    frames = []

    print("🔎 Looking for data files...")

    if not DATA_FOLDER.exists():
        print("⚠ data/ folder missing.")
        return pd.DataFrame()

    for file in DATA_FOLDER.glob("*.csv"):
        print(f"📄 Loading {file.name}...")
        try:
            df = pd.read_csv(file, on_bad_lines="skip")

            # Validate columns
            if not {"timestamp", "kwh"}.issubset(df.columns):
                print(f"Skipped: {file.name} (missing required columns)")
                continue

            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp", "kwh"])

            # Assign building name if missing
            if "building" not in df.columns:
                df["building"] = file.stem

            # Add month column for convenience
            df["month"] = df["timestamp"].dt.to_period("M").astype(str)

            frames.append(df)

        except Exception as err:
            print(f"❌ Couldn't load {file.name}: {err}")

    if not frames:
        print("⚠ No usable CSV files detected.")
        return pd.DataFrame()

    print("✅ Data load complete.")
    return pd.concat(frames, ignore_index=True)


# ==============================
# AGGREGATION FUNCTIONS
# ==============================

def compute_daily(df):
    df = df.copy().set_index("timestamp")
    return df.groupby("building")["kwh"].resample("D").sum().reset_index()


def compute_weekly(df):
    df = df.copy().set_index("timestamp")
    return df.groupby("building")["kwh"].resample("W").sum().reset_index()


def summarize_buildings(df):
    return df.groupby("building")["kwh"].agg(
        total_kwh="sum",
        mean_kwh="mean",
        min_kwh="min",
        max_kwh="max"
    ).reset_index()


# ==============================
# VISUAL DASHBOARD
# ==============================

def build_visuals(df, daily, weekly):
    if df.empty:
        print("⚠ No data to visualize.")
        return

    fig, axes = plt.subplots(3, 1, figsize=(11, 16))
    fig.suptitle("Campus Energy Dashboard", fontsize=15)

    # LINE PLOT – Daily Trend
    ax1 = axes[0]
    for bname, group in daily.groupby("building"):
        ax1.plot(group["timestamp"], group["kwh"], marker="o", label=bname)

    ax1.set_title("Daily Usage Trend")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")
    ax1.legend()
    ax1.grid(True)

    # BAR CHART – Weekly Average Usage
    ax2 = axes[1]
    weekly_avg = weekly.groupby("building")["kwh"].mean().reset_index()
    ax2.bar(weekly_avg["building"], weekly_avg["kwh"])
    ax2.set_title("Weekly Avg Consumption")
    ax2.set_ylabel("kWh")

    # SCATTER PLOT – Hour vs kWh
    ax3 = axes[2]
    df_temp = df.copy()
    df_temp["hour"] = df_temp["timestamp"].dt.hour
    ax3.scatter(df_temp["hour"], df_temp["kwh"])
    ax3.set_title("Hourly Load Distribution")
    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("kWh")

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    out = EXPORT_FOLDER / "dashboard.png"
    plt.savefig(out)
    plt.close()
    print(f"📊 Dashboard saved to {out}")


# ==============================
# EXPORT REPORTS
# ==============================

def export_results(clean_df, summary_df, manager_obj):
    """Save cleaned dataset, building summary & a readable summary file."""

    # Save cleaned dataset
    cleaned_path = EXPORT_FOLDER / "cleaned_energy_data.csv"
    clean_df.to_csv(cleaned_path, index=False)
    print(f"💾 Cleaned data saved: {cleaned_path}")

    # Save summary table
    summary_path = EXPORT_FOLDER / "building_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"💾 Summary table saved: {summary_path}")

    # Executive Summary
    total_usage = clean_df["kwh"].sum()
    highest_building = summary_df.loc[summary_df["total_kwh"].idxmax()]

    # Find peak timestamp
    peak = clean_df.loc[clean_df["kwh"].idxmax()]

    daily = compute_daily(clean_df)
    weekly = compute_weekly(clean_df)

    lines = [
        "Campus Energy Report",
        "====================",
        f"Total campus usage: {total_usage:.2f} kWh\n",
        f"Highest consuming building: {highest_building['building']} ({highest_building['total_kwh']:.2f} kWh)\n",
        "Peak Load Info:",
        f"  Building: {peak['building']}",
        f"  Time: {peak['timestamp']}",
        f"  Value: {peak['kwh']:.2f} kWh\n",
        "Recorded Periods:",
        f"  Unique days: {daily['timestamp'].dt.date.nunique()}",
        f"  Unique weeks: {weekly['timestamp'].dt.isocalendar().week.nunique()}",
    ]

    summary_file = EXPORT_FOLDER / "summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"📝 Summary written to {summary_file}")


# ==============================
# MAIN PROGRAM FLOW
# ==============================

def main():
    print("🚀 Energy Dashboard Initializing...")

    df = read_energy_data()
    if df.empty:
        print("❌ No data found. Exiting.")
        return

    daily = compute_daily(df)
    weekly = compute_weekly(df)
    summary = summarize_buildings(df)

    manager = CampusEnergyManager()
    manager.populate_from_df(df)

    build_visuals(df, daily, weekly)
    export_results(df, summary, manager)

    print("🎉 Dashboard generation complete.")


if __name__ == "__main__":
    main()
