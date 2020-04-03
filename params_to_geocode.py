def get_size(lowercorner, uppercorner):
    lon1, lat1 = lowercorner.split()
    lon2, lat2 = uppercorner.split()
    longitude, lattitude = float(lon2) - float(lon1), float(lat2) - float(lat1)
    return str(longitude / 2), str(lattitude / 2)