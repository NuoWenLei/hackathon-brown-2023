def locationVerifier(newLong, newLat, placeLong, placeLat):
    meterToCoord = 1 / 111000
    lat_cond = placeLat - 10 * meterToCoord <= newLat <= 10 * meterToCoord + placeLat
    long_cond = placeLong - 10 * meterToCoord <= newLong <= 10 * meterToCoord + placeLong
    return (lat_cond and long_cond)
