import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error


# Figure 1: Compares observed and predicted duration over a coordinate plane with a reference y=x line
radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")

df_coords = df[["real_duration", "predicted_duration"]]

df_coords.plot.scatter(x="real_duration", y="predicted_duration", color="blue", title="Observed vs Predicted Duration")

plt.axline((0, 0), slope=1, color="red", linestyle="--", label="y=x")

plt.title("Observed vs Predicted Duration", fontsize=18)
plt.xlabel("Observed Duration (hr)", fontsize=16)
plt.ylabel("Predicted Duration (hr)", fontsize=16)

plt.show()


# Figure 2: Compares RMSE, MAE, and Mean Error for each route with at least 5 voyages in a bar graph
radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")

df["route"] = df.apply(
    lambda row: " ↔ ".join(sorted([row["end_port"], row["start_port"]])),
    axis=1
)

df["prediction_error"] = df["real_duration"] - df["predicted_duration"]

route_results = []
for route, group in df.groupby("route"):

    if len(group) < 5:
        continue
    route_mse = mean_squared_error(group["real_duration"], group["predicted_duration"])
    route_mae = mean_absolute_error(group["real_duration"], group["predicted_duration"])
    print(f"Route: {route}, Length: {len(group)}, MSE: {route_mse}, MAE: {route_mae}, Mean Error: {group['prediction_error'].mean()}")
    route_results.append({
        "route": route,
        "rmse": np.sqrt(route_mse),
        "mae": route_mae,
        "mean_error": group["prediction_error"].mean(),
    })

x = np.arange(len(route_results))
width = 0.25

plt.bar(
    x - width,
    [result["rmse"] for result in route_results],
    width,
    label="RMSE"
)

plt.bar(
    x,
    [result["mae"] for result in route_results],
    width,
    label="MAE"
)

plt.bar(
    x + width,
    [result["mean_error"] for result in route_results],
    width,
    label="Mean Error"
)

plt.xlabel("Route", fontsize=16)
plt.ylabel("Error (hours)", fontsize=16)
plt.title("Prediction Error by Route", fontsize=18)

plt.xticks(
    x,
    [result["route"] for result in route_results],
    rotation=45,
    ha="right"
)

plt.axhline(0, linewidth=0.8)

plt.legend()
plt.tight_layout()
plt.show()