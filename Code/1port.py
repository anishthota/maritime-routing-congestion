import pandas as pd

def convert_to_decimal_degrees(coord):
    coord = list(str(coord))
    degrees = int("".join(coord[0:coord.index('°')]))
    minutes = int("".join(coord[coord.index('°') + 1: coord.index("'")]))
    seconds = int("".join(coord[coord.index("'") + 1:coord.index('"')]))
    direction = coord[-1]

    decimal_degrees = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees

    return decimal_degrees

# Convert the World Port Index's default coordinates from degrees, minutes, seconds to decimal degrees
df_ports = pd.read_csv("Data/Cleaned/world_port_index.csv")
df_ports['latitude'] = df_ports['latitude'].apply(convert_to_decimal_degrees)
df_ports['longitude'] = df_ports['longitude'].apply(convert_to_decimal_degrees)
df_ports.to_csv("Data/Cleaned/world_port_index.csv", index=False)