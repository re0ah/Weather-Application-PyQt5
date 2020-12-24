from requests import get
import geocoder

def current_location():
	geodata = geocoder.ip("me")
	geodata = geodata.latlng
	return {"lat": geodata[0],
			"lon": geodata[1]}