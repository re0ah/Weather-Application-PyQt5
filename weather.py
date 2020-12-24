import requests
import os
from datetime import datetime
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import QSize
from PyQt5.QtXml import QDomDocument
from PyQt5.QtSvg import QSvgRenderer
import rgb

API_KEY = "da57d2738ca74db4edc3a113a59b7423"
def now(lat, lon):
	addr = f"https://api.openweathermap.org/data/2.5/weather?"\
				f"lang=RU&"\
				f"units=metric&"\
				f"lat={str(lat)}&"\
				f"lon={str(lon)}&"\
				f"appid={API_KEY}"
	request = requests.get(addr)
	return request.json()

def week(lat, lon):
	#https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid=da57d2738ca74db4edc3a113a59b7423
	addr = f"https://api.openweathermap.org/data/2.5/onecall?"\
				f"lang=RU&"\
				f"dt=7&"\
				f"units=metric&"\
				f"exclude=daily&"\
				f"lat={str(lat)}&"\
				f"lon={str(lon)}&"\
				f"appid={API_KEY}"
	request = requests.get(addr)
	json = request.json()
	return json["daily"]

def get(lat, lon):
	w = {}
	w["daily"] = week(lat, lon)
	w["now"] = now(lat, lon)
	for i in range(7):
		#that all need for access by same keys on "daily" and "now" 
		w["daily"][i]["name"] = w["now"]["name"]
		w["daily"][i]["main"] = {}
		w["daily"][i]["main"]["temp"] = w["daily"][i]["temp"]["day"]
		w["daily"][i]["main"]["feels_like"] = w["daily"][i]["feels_like"]["day"]
		w["daily"][i]["main"]["temp_min"] = w["daily"][i]["temp"]["min"]
		w["daily"][i]["main"]["temp_max"] = w["daily"][i]["temp"]["max"]
		w["daily"][i]["wind"] = {}
		w["daily"][i]["wind"]["speed"] = w["daily"][i]["wind_speed"]
		w["daily"][i]["wind"]["deg"] = w["daily"][i]["wind_deg"]
	return w

def wind_direction(deg):
	if ((deg >= 338) & (deg <= 360)) |\
	   ((deg >= 0)   & (deg <  23)):
		return "Ветер северный"
	elif (deg >= 23) & (deg < 68):
		return "Ветер северо-восточный"
	elif (deg >= 68) & (deg < 113):
		return "Ветер восточный"
	elif (deg >= 113) & (deg < 158):
		return "Ветер южно-восточный"
	elif (deg >= 158) & (deg < 203):
		return "Ветер южный"
	elif (deg >= 203) & (deg < 248):
		return "Ветер южно-западный"
	elif (deg >= 248) & (deg < 293):
		return "Ветер западный"
	elif (deg >= 293) & (deg < 338):
		return "Ветер северо-западный"
	else:
		return "Ветер ???"

def weather_icon(weather_id, temperature):
	hour = datetime.now().hour
	weather_directory = "weather_icons"
	if (hour >= 0) & (hour < 6):
		weather_directory = os.path.join(weather_directory, "night")
	elif (hour >= 6) & (hour < 12):
		weather_directory = os.path.join(weather_directory, "morning_evening")
	elif (hour >= 12) & (hour < 18):
		weather_directory = os.path.join(weather_directory, "day")
	elif (hour >= 18) & (hour < 24):
		weather_directory = os.path.join(weather_directory, "morning_evening")
	os.chdir(weather_directory)

	if weather_id == 200: #Thunderstorm, thunderstorm with light rain
		svg_fname = "storm-showers.svg"
	elif weather_id == 201: #Thunderstorm, thunderstorm with rain
		svg_fname = "thunderstorm.svg"
	elif weather_id == 202: #Thunderstorm, thunderstorm with heavy rain
		svg_fname = "thunderstorm.svg"
	elif weather_id == 210: #Thunderstorm, light thunderstorm
		svg_fname = "storm-showers.svg"
	elif weather_id == 211: #Thunderstorm, thunderstorm
		svg_fname = "thunderstorm.svg"
	elif weather_id == 212: #Thunderstorm, heavy thunderstorm
		svg_fname = "thunderstorm.svg"
	elif weather_id == 221: #Thunderstorm, ragged thunderstorm
		svg_fname = "thunderstorm.svg"
	elif weather_id == 230: #Thunderstorm, thunderstorm with light drizzle 
		svg_fname = "storm-showers.svg"
	elif weather_id == 231: #Thunderstorm, thunderstorm with drizzle
		svg_fname = "storm-showers.svg"
	elif weather_id == 232: #Thunderstorm, thunderstorm with heavy drizzle 
		svg_fname = "thunderstorm.svg"

	elif weather_id == 300: #Drizzle, light intensity drizzle 
		svg_fname = "showers.svg"
	elif weather_id == 301: #Drizzle, drizzle 
		svg_fname = "showers.svg"
	elif weather_id == 302: #Drizzle, heavy intensity drizzle
		svg_fname = "rain.svg"
	elif weather_id == 310: #Drizzle, light intensity drizzle rain 
		svg_fname = "showers.svg"
	elif weather_id == 311: #Drizzle, drizzle rain 
		svg_fname = "showers.svg"
	elif weather_id == 312: #Drizzle, heavy intensity drizzle rain 
		svg_fname = "rain.svg"
	elif weather_id == 313: #Drizzle, shower rain and drizzle 
		svg_fname = "showers.svg"
	elif weather_id == 314: #Drizzle, heavy shower rain and drizzle 
		svg_fname = "rain.svg"
	elif weather_id == 321: #Drizzle, shower drizzle
		svg_fname = "showers.svg"

	elif weather_id == 500: #Rain, light rain
		svg_fname = "showers.svg"
	elif weather_id == 501: #Rain, moderate rain
		svg_fname = "rain.svg"
	elif weather_id == 502: #Rain, heavy intensity rain
		svg_fname = "rain.svg"
	elif weather_id == 503: #Rain, very heavy rain
		svg_fname = "rain.svg"
	elif weather_id == 504: #Rain, extreme rain
		svg_fname = "rain.svg"
	elif weather_id == 511: #Rain, freezing rain
		svg_fname = "rain.svg"
	elif weather_id == 520: #Rain, light intensity shower rain
		svg_fname = "showers.svg"
	elif weather_id == 521: #Rain, shower rain
		svg_fname = "showers.svg"
	elif weather_id == 522: #Rain, heavy intensity shower rain
		svg_fname = "rain.svg"
	elif weather_id == 531: #Rain, ragged shower rain
		svg_fname = "rain.svg"

	elif weather_id == 600: #Snow, light snow
		svg_fname = "snow.svg"
	elif weather_id == 601: #Snow, Snow
		svg_fname = "snow.svg"
	elif weather_id == 602: #Snow, Heavy snow
		svg_fname = "snow.svg"
	elif weather_id == 611: #Snow, Sleet
		svg_fname = "snow.svg"
	elif weather_id == 612: #Snow, Light shower sleet
		svg_fname = "snow.svg"
	elif weather_id == 613: #Snow, Shower sleet
		svg_fname = "snow.svg"
	elif weather_id == 615: #Snow, Light rain and snow
		svg_fname = "snow.svg"
	elif weather_id == 616: #Snow, Rain and snow
		svg_fname = "snow.svg"
	elif weather_id == 620: #Snow, Light shower snow
		svg_fname = "snow.svg"
	elif weather_id == 621: #Snow, Shower snow
		svg_fname = "snow.svg"
	elif weather_id == 622: #Snow, Heavy shower snow
		svg_fname = "snow.svg"

	elif weather_id == 701: #Mist, mist
		svg_fname = "fog.svg"
	elif weather_id == 711: #Smoke, Smoke
		svg_fname = "fog.svg"
	elif weather_id == 721: #Haze, Haze
		svg_fname = "fog.svg"
	elif weather_id == 731: #Dust, sand/dust whirls
		svg_fname = "fog.svg"
	elif weather_id == 741: #Fog, Fog
		svg_fname = "fog.svg"
	elif weather_id == 751: #Sand, sand
		svg_fname = "fog.svg"
	elif weather_id == 761: #Dust, Dust
		svg_fname = "dust.svg"
	elif weather_id == 762: #Ash, volcanic ash
		svg_fname = "ccloudy.svg"
	elif weather_id == 771: #Squall, squalls
		svg_fname = "ccloudy.svg"
	elif weather_id == 781: #Tornado, Tornado
		svg_fname = "tornado.svg"

	elif weather_id == 800: #Clear, clear sky
		svg_fname = "clear.svg"
	elif weather_id == 801: #Clouds, few clouds: 11-25% 
		svg_fname = "ccloudy.svg"
	elif weather_id == 802: #Clouds, scattered clouds: 25-50%
		svg_fname = "ccloudy.svg"
	elif weather_id == 803: #Clouds, broken clouds: 51-84% 
		svg_fname = "cloudy.svg"
	elif weather_id == 804: #Clouds, overcast clouds: 85-100%
		svg_fname = "cloudy.svg"

	pixmap = svg_to_pixmap(svg_fname, temperature)
	
	os.chdir(os.path.join("..", ".."))

	return pixmap

def svg_to_pixmap(fname, temperature):
	def SetAttrRecur(elem, strtagname, strattr, strattrval):
		if (elem.tagName() == strtagname):
			elem.setAttribute(strattr, strattrval)
		for i in range(elem.attributes().count()):
			if (elem.childNodes().at(i).isElement() == False):
			    continue
			SetAttrRecur(elem.childNodes().at(i).toElement(), strtagname, strattr, strattrval)

	t = QDomDocument()
	with open(fname) as f:
		t.setContent(f.read())
	SetAttrRecur(t.documentElement(), "path", "fill", rgb.get_fg_temperature(temperature))
	
	renderer = QSvgRenderer(t.toByteArray())
	pixmap = QPixmap(QSize(160, 160))
	pixmap.fill(QColor("#000000ff"))
	painter = QPainter(pixmap)
	renderer.render(painter)
	painter.end()

	return pixmap
