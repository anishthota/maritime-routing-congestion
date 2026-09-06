from pathlib import Path
import pandas as pd
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    EARTH_RADIUS = 6371  # radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance

ais_folder = Path("Data/Raw/AIS-Traffic")

PORT_RADII = [10, 15, 20]
radius_trackers = {}
for radius in PORT_RADII:
    radius_trackers[radius] = {
        "port_begins": {},
        "port_ends": {},
        "start": {},
        "dest": {},
        "trajectories": {},
        "trips": {}
    }

df_ports = pd.read_csv("Data/Cleaned/world_port_index.csv")

for radius in PORT_RADII: # Conducts the radius sensitivity analysis by running the trip construction process for each radius (10 km, 15 km, and 20 km)
    tracker = radius_trackers[radius]
    for file in sorted(ais_folder.glob("*.csv.zst")):
        df = pd.read_csv(file)

        df = df[["mmsi", "base_date_time", "longitude", "latitude", "sog", "vessel_type"]]
        df = df[(df["vessel_type"] >= 70) & (df["vessel_type"] <= 79)] # Filter for only cargo vessels (AIS vessel types 70-79)


        df_sorted = df.sort_values(by = ["mmsi", "base_date_time"]) # Sort AIS broadcast data chronologically for every vessel

        for row in df_sorted.itertuples():
            mmsi = row.mmsi
            timestamp = row.base_date_time
            lat = row.latitude
            lon = row.longitude

            if mmsi in tracker["trips"]:
                continue
            
            near_port = True

            for port_row in df_ports.itertuples():
                port_name = port_row.port_name
                port_lat = port_row.latitude
                port_lon = port_row.longitude

                distance = haversine_distance(port_lat, port_lon, lat, lon)

                if distance < radius:
                    # Ends a vessel's trip if it is near a different port than the one it started from
                    if mmsi in tracker["trajectories"] and port_name != tracker["start"][mmsi]:
                        tracker["trips"][mmsi] = tracker["trajectories"][mmsi]
                        del tracker["trajectories"][mmsi]
                        tracker["dest"][mmsi] = port_name
                        near_port = False

                        if port_name in tracker["port_ends"]:
                            tracker["port_ends"][port_name] += 1
                        else:
                            tracker["port_ends"][port_name] = 1
                        break
                    # Begins a vessel's trip if it is near a port and has not started a trip yet
                    else:
                        tracker["start"][mmsi] = port_name
                        tracker["trajectories"][mmsi] = [(timestamp, lat, lon)]
                        near_port = False
                        if port_name in tracker["port_begins"]:
                            tracker["port_begins"][port_name] += 1
                        else:
                            tracker["port_begins"][port_name] = 1
                        break
            # Appends broadcast data to a vessel's trajectory while it's not near a port
            if mmsi in tracker["trajectories"] and near_port:
                tracker["trajectories"][mmsi].append((timestamp, lat, lon))

    output = []
    for mmsi in tracker["trips"]:
        output.append({
            "mmsi": mmsi,
            "start_port": tracker["start"][mmsi],
            "end_port": tracker["dest"][mmsi],
            "trajectory": tracker["trips"][mmsi]
        })
    filename = f"Data/Working/cleaned_trajectories_{radius}km.csv"

    pd.DataFrame(output).to_csv(
        filename,
        index=False
    )