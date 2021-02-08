def get_spn(envelope):
    envelope = envelope["response"]["GeoObjectCollection"][
        'featureMember'][0]['GeoObject']['boundedBy']['Envelope']
    lower_corner1, lower_corner2 = map(float, envelope['lowerCorner'].split())
    upper_corner1, upper_corner2 = map(float, envelope['upperCorner'].split())
    longitude = abs(lower_corner1 - upper_corner1)
    lattitude = abs(lower_corner2 - upper_corner2)
    return str(longitude), str(lattitude)
