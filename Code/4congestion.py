import rasterio
import numpy as np
from pyproj import Transformer
import pandas as pd
import ast


def separate_traj(trajectory):
    if isinstance(trajectory, str):
        trajectory = ast.literal_eval(trajectory)
    if len(trajectory) < 2:
        return -1
    return trajectory

radius = 15 # km
df = pd.read_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv")

congestion_raster_path = "Data/Raw/AIS Transit/ais-transit-count-2025.tif"

with rasterio.open(congestion_raster_path) as src:

    # Transforms coordinates from WGS84 to the raster's coordinate reference system
    transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)

    for row in df.itertuples():

        trajectory = row.trajectory
        trajectory = separate_traj(trajectory)

        if trajectory == -1:
            continue

        congestion_values = []

        for (timestamp, lat, lon) in trajectory:

            x, y = transformer.transform(lon, lat)
            congestion_value = next(src.sample([(x, y)]))[0]

            if congestion_value is not None and not np.isnan(congestion_value):
                congestion_values.append(congestion_value)


        if len(congestion_values) == 0:
            avg_congestion = np.nan
            median_congestion = np.nan
            max_congestion = np.nan
        else:
            avg_congestion = np.nanmean(congestion_values)
            median_congestion = np.nanmedian(congestion_values)
            max_congestion = np.nanmax(congestion_values)


        df.at[row.Index, 'avg_congestion'] = avg_congestion
        df.at[row.Index, 'median_congestion'] = median_congestion
        df.at[row.Index, 'max_congestion'] = max_congestion
        df.at[row.Index, 'n_points_sampled'] = len(congestion_values)

df = df[
    (df["real_duration"] > 3) &
    (df["n_points_sampled"] > 10)
].copy()

df.to_csv(f"Data/Working/cleaned_trajectories_{radius}km.csv", index=False)