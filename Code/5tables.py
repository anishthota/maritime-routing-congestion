import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import pearsonr

# Table 1: Summarizes the predicted and real durations, prediction error, and congestion metrics for all voyages
radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")

df["prediction_error"] = df["real_duration"] - df["predicted_duration"]

variables = {
    "Predicted duration": "predicted_duration",
    "Observed duration": "real_duration",
    "Prediction error": "prediction_error",
    "Mean congestion": "avg_congestion",
    "Median congestion": "median_congestion",
    "Maximum congestion": "max_congestion"
}

rows = []
for label, column in variables.items():
    series = df[column].dropna()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    rows.append({
        "Variable": label,
        "N": len(series),
        "Mean": series.mean(),
        "SD": series.std(),
        "Median": series.median(),
        "IQR": q3 - q1,
        "Minimum": series.min(),
        "Maximum": series.max()
    })

summary = pd.DataFrame(rows)
summary.to_csv("Data/Final/summary_stats.csv", index=False)

# Table 2: Compares voyage count, RMSE, MAE, and Mean Error for each route with at least 5 voyages
radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")

df["route"] = (
    np.sort(df[["start_port", "end_port"]], axis=1)[:, 0]
    + " ↔ "
    + np.sort(df[["start_port", "end_port"]], axis=1)[:, 1]
)
df["prediction_error"] = df["real_duration"] - df["predicted_duration"]

route_results = []
for route, group in df.groupby("route"):

    if len(group) < 5:
        continue
    route_mse = mean_squared_error(group["real_duration"], group["predicted_duration"])
    route_mae = mean_absolute_error(group["real_duration"], group["predicted_duration"])
    print(f"Route: {route}, Length: {len(group)}, MSE: {route_mse}, MAE: {route_mae}")
    route_results.append({
        "route": route,
        "voyages": len(group),
        "rmse": np.sqrt(route_mse),
        "mae": route_mae,
        "mean_error": group["prediction_error"].mean(),
    })

route_df = pd.DataFrame(route_results)
route_df.to_csv("Data/Final/route_results.csv", index=False)

# Table 3: Summarizes Pearson's correlation coefficients and p-values between three congestion metrics and prediction error
radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")
df["prediction_error"] = df["real_duration"] - df["predicted_duration"]

avg_r, avg_p = pearsonr(df["avg_congestion"], df["prediction_error"])
median_r, median_p = pearsonr(df["median_congestion"], df["prediction_error"])
max_r, max_p = pearsonr(df["max_congestion"], df["prediction_error"])
correlations = pd.DataFrame({
    "metric": [
        "avg_congestion", "max_congestion", "median_congestion"
    ],
    "pearson_r": [
        avg_r,
        max_r,
        median_r
    ],
    "p_value": [
        avg_p,
        max_p,
        median_p
    ]
})
correlations.to_csv("Data/Final/correlation_results.csv", index=False)

# Table 4: Compares different port radii used in the analysis and their corresponding voyage counts, MSE, RMSE, MAE, and Mean Error
summary = pd.DataFrame(columns=["Radius", "Voyages", "MSE", "RMSE", "MAE", "Mean Error"])
for i in [10, 15, 20]:
    df = pd.read_csv(f"Data/Working/cleaned_trajectories_{i}km.csv")

    mse = mean_squared_error(df["real_duration"], df["predicted_duration"])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(df["real_duration"], df["predicted_duration"])
    df["prediction_error"] = df["real_duration"] - df["predicted_duration"]
    mean_error = df["prediction_error"].mean()
    summary = pd.concat([summary, pd.DataFrame({
        "Radius": [f"{i} km"],
        "Voyages": len(df),
        "MSE": [mse],
        "RMSE": [rmse],
        "MAE": [mae],
        "Mean Error": [mean_error]
    })], ignore_index=True)

summary.to_csv("Data/Final/radius_comparison.csv", index=False)

# Table 5: Compares different constant speeds used in the analysis and their corresponding MSE, RMSE, MAE, and Mean Error
summary = pd.DataFrame(columns=["Speed", "MSE", "RMSE", "MAE", "Mean Error"])
for i in [10, 12, 14, 16]:
    df = pd.read_csv(f"Data/Working/cleaned_trajectories_15km_{i}knots.csv")

    mse = mean_squared_error(df["real_duration"], df["predicted_duration"])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(df["real_duration"], df["predicted_duration"])
    df["prediction_error"] = df["real_duration"] - df["predicted_duration"]
    mean_error = df["prediction_error"].mean()
    summary = pd.concat([summary, pd.DataFrame({
        "Speed": [f"{i} knots"],
        "MSE": [mse],
        "RMSE": [rmse],
        "MAE": [mae],
        "Mean Error": [mean_error]
    })], ignore_index=True)

summary.to_csv("Data/Final/speed_comparison.csv", index=False)

# Table 6: Contains a list of selected ports used in the analysis, along with their identifiers, latitudes, and longitudes taken from the World Port Index
# Created manually through the World Port Index and saved as a CSV file