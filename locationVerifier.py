import what3words

geocoder = what3words.Geocoder("78P5ZDMW")
def locationVerifier(newLong, newLat, placeLong, placeLat):
    new3words = geocoder.convert_to_3wa(what3words.Coordinates(newLat, newLong))
    place3words = geocoder.convert_to_3wa(what3words.Coordinates(placeLat, placeLong))
    return new3words == place3words

def locationToW3W(lon, lat):
    return geocoder.convert_to_3wa(what3words.Coordinates(lat, lon))

print(locationVerifier(51.521251, 0.203586, 51.521251, 0.203583))
