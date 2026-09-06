import pandas as pd
import searoute as sr
from datetime import datetime
import ast

radius = 15 # km
PREDICTION_CONSTANT_SPEED = 14 # knots

df = pd.read_csv(f'Data/Working/cleaned_trajectories_{radius}km.csv')

def separate_traj(trajectory):
    if isinstance(trajectory, str):
        trajectory = ast.literal_eval(trajectory)
    if len(trajectory) < 2:
        return -1
    return trajectory

for row in df.itertuples():
    trajectory = row.trajectory
    trajectory = separate_traj(trajectory)

    if trajectory == -1:
        continue

    # Calculates the observed duration of a trip based on the timestamps of the first and last points in the trajectory
    start_time = datetime.strptime(trajectory[0][0], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(trajectory[-1][0], '%Y-%m-%d %H:%M:%S')
    observed_duration = (end_time - start_time).total_seconds() / 3600

    start_point = trajectory[0][1:][::-1]
    end_point = trajectory[-1][1:][::-1]

    # Predicts the duration of the trip using Dijkstra's algorithm, the first and last points of the trajectory, and a constant speed
    route = sr.searoute(start_point, end_point, units="naut", speed_knot = PREDICTION_CONSTANT_SPEED)

    df.at[row.Index, 'predicted_duration'] = route.properties['duration_hours']
    df.at[row.Index, 'real_duration'] = observed_duration

df.to_csv(f'Data/Working/cleaned_trajectories_{radius}km_{PREDICTION_CONSTANT_SPEED}knots.csv', index=False)