import math

def heuristic_haversine(id_atual, id_destino, coordinates):
    lat1, lon1 = coordinates[id_atual]["lat"], coordinates[id_atual]["lon"]
    lat2, lon2 = coordinates[id_destino]["lat"], coordinates[id_destino]["lon"]

    R = 6371.0  #raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c