# =============================================================
#  Name:  Kartavya Gautam
#  Roll No: 2501410024
#  Course: B.Tech CSE (Cybersecurity)
#  Section: A
#  Project: WEATHER DATA VISUALIZER
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------------
# Helper Functions – Makes the code cleaner and easier to read
# -------------------------------------------------------------

def load_dataset(filename):
    """
    Loads the weather CSV file and prints its basic structure.
    This includes head(), info(), and describe(), as required.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError("❌ weather.csv is missing! Please download a real dataset first.")

    data = pd.read_csv(filename)

    print("\n📌 Dataset Loaded Successfully!")

    print("\n👉 First 5 rows of the dataset:")
    print(data.head())

    print("\n👉 Dataset Information:")
    print(data.info())

    print("\n👉 Statistical Summary:")
    print(data.describe())

    return data


def clean_dataset(data):
    """
    Cleans and prepares the dataset for analysis.
    - Converts the Date column to datetime format
    - Removes rows with missing values
    - Keeps only the relevant columns
    """
    print("\n🧹 Cleaning the dataset...")

    # Convert Date column into proper datetime format
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    # Drop rows where Date is invalid or empty
    data = data.dropna(subset=["Date"])

    # Keep only the required columns
    needed_columns = ["Date", "Temperature", "Rainfall", "Humidity"]
    available_columns = [col for col in needed_columns if col in data.columns]

    data = data[available_columns]

    print("✅ Dataset cleaned successfully!")
    return data


def compute_statistics(data):
    """
    Computes all required statistics using NumPy.
    Also performs monthly and yearly grouping.
    """
    print("\n📊 Computing important statistics...")

    stats = {
        "Average Temperature": np.mean(data["Temperature"]),
        "Maximum Temperature": np.max(data["Temperature"]),
        "Minimum Temperature": np.min(data["Temperature"]),
        "Temperature Standard Deviation": np.std(data["Temperature"])
    }

    print("\n🌡️ Temperature Statistics:")
    for label, value in stats.items():
        print(f"{label}: {value}")

    # Add Month & Year columns for grouping
    data["Month"] = data["Date"].dt.month
    data["Year"] = data["Date"].dt.year

    # Monthly summary statistics
    monthly_summary = data.groupby("Month").agg({
        "Temperature": ["mean", "max", "min"],
        "Rainfall": "sum"
    })

    # Yearly summary statistics
    yearly_summary = data.groupby("Year").agg({
        "Temperature": ["mean", "max", "min"],
        "Rainfall": "sum"
    })

    print("\n📅 Monthly Summary:")
    print(monthly_summary)

    print("\n📆 Yearly Summary:")
    print(yearly_summary)

    return stats, monthly_summary, yearly_summary


def create_visualizations(data):
    """
    Creates all required visualizations:
    - Daily Temperature Line Plot
    - Monthly Rainfall Bar Chart
    - Humidity vs Temperature Scatter Plot
    - Combined Plot (for bonus marks)
    """
    print("\n📈 Creating visualizations...")

    # ---------------------------------------------------------
    # Line Chart – Temperature Trend
    # ---------------------------------------------------------
    plt.figure()
    plt.plot(data["Date"], data["Temperature"])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig("temperature_trend.png")
    plt.show()

    # ---------------------------------------------------------
    # Bar Chart – Monthly Rainfall
    # ---------------------------------------------------------
    monthly_rainfall = data.groupby(data["Date"].dt.month)["Rainfall"].sum()
    plt.figure()
    monthly_rainfall.plot(kind="bar")
    plt.title("Total Monthly Rainfall")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()
    plt.savefig("monthly_rainfall.png")
    plt.show()

    # ---------------------------------------------------------
    # Scatter Plot – Humidity vs Temperature
    # ---------------------------------------------------------
    plt.figure()
    plt.scatter(data["Temperature"], data["Humidity"])
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    plt.savefig("humidity_vs_temperature.png")
    plt.show()

    # ---------------------------------------------------------
    # Combined Subplot Figure (Bonus Marks!)
    # ---------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(data["Date"], data["Temperature"], color='blue')
    axes[0].set_title("Temperature Trend")

    axes[1].scatter(data["Temperature"], data["Humidity"], color='green')
    axes[1].set_title("Temperature vs Humidity")

    plt.tight_layout()
    plt.savefig("combined_plot.png")
    plt.show()

    print("✅ All plots created and saved!")


def export_results(data, stats):
    """
    Saves the cleaned dataset and summary report.
    """
    data.to_csv("cleaned_weather.csv", index=False)

    with open("summary.txt", "w") as f:
        f.write("Weather Data Analysis Summary\n")
        f.write("==============================\n\n")
        for label, value in stats.items():
            f.write(f"{label}: {value}\n")

    print("📁 Cleaned dataset and summary report exported successfully!")


# -------------------------------------------------------------
# Main Program Flow – Executes all steps in order
# -------------------------------------------------------------

filename = "weather.csv"  # Make sure this file exists in your folder!

# Step 1: Load the dataset
raw_data = load_dataset(filename)

# Step 2: Clean the dataset
clean_data = clean_dataset(raw_data)

# Step 3: Compute statistics
stats, monthly, yearly = compute_statistics(clean_data)

# Step 4: Generate visualizations
create_visualizations(clean_data)

# Step 5: Export final results
export_results(clean_data, stats)

print("\n🎉 All tasks completed successfully! Your project is ready to submit.")
