from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
import weather
from datetime import datetime
import rgb
import rgba
from count_date import Count_Date

class Maximize_window(QWidget):
	def __init__(self, app, mainw, min_wnd):
		self.app = app
		self.mainw = mainw
		self.min_wnd = min_wnd
		super().__init__(None, Qt.WindowFlags())
		self.init_window()
		self.update_info(self.mainw.weather_info["now"])

	def init_window(self):
		self.ui = uic.loadUi("maximize.ui")
		self.ui.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.ui.closeEvent = self.closeEvent
		self.ui.btn_roll_up.clicked.connect(self.minimize)
		self.ui.show()
		self.lbl_list = [self.ui.lbl_city, self.ui.lbl_weather_desc, self.ui.lbl_time,
						 self.ui.lbl_ctemp, self.ui.lbl_ctemp_feel, self.ui.lbl_temp,
						 self.ui.lbl_temp_feel, self.ui.lbl_cwind_v, self.ui.lbl_wind_deg,
						 self.ui.lbl_wind_v, self.ui.lbl_date_1, self.ui.lbl_date_2,
						 self.ui.lbl_date_3, self.ui.lbl_date_4, self.ui.lbl_date_5,
						 self.ui.lbl_date_6, self.ui.lbl_date_7, self.ui.min_temp_date_1,
						 self.ui.min_temp_date_2, self.ui.min_temp_date_3, self.ui.min_temp_date_4, 
						 self.ui.min_temp_date_5, self.ui.min_temp_date_6, self.ui.min_temp_date_7, 
						 self.ui.max_temp_date_1, self.ui.max_temp_date_2, self.ui.max_temp_date_3,
						 self.ui.max_temp_date_4, self.ui.max_temp_date_5, self.ui.max_temp_date_6,
						 self.ui.max_temp_date_7]

		self.ui.btn_date_1.clicked.connect(self.choose_day_1)
		self.ui.btn_date_2.clicked.connect(self.choose_day_2)
		self.ui.btn_date_3.clicked.connect(self.choose_day_3)
		self.ui.btn_date_4.clicked.connect(self.choose_day_4)
		self.ui.btn_date_5.clicked.connect(self.choose_day_5)
		self.ui.btn_date_6.clicked.connect(self.choose_day_6)
		self.ui.btn_date_7.clicked.connect(self.choose_day_7)
		

	def minimize(self):
		self.ui.hide()
		self.min_wnd.show_wnd()

	def update_info(self, weather_info):
		weather_desc = weather_info["weather"][0]["description"].capitalize()
		self.ui.lbl_weather_desc.setText(weather_desc)

		self.ui.lbl_city.setText(f"г. {weather_info['name']}")
		
		temp = str(round(weather_info["main"]["temp_min"]))
		self.ui.lbl_temp.setText(f"{temp}°C")

		temp_feel = str(round(weather_info["main"]["feels_like"]))
		self.ui.lbl_temp_feel.setText(f"{temp_feel}°C")

		weather_icon = weather.weather_icon(weather_info["weather"][0]["id"], int(temp))
		self.ui.lbl_weather_icon.setPixmap(weather_icon)

		wind_speed = str(int(weather_info["wind"]["speed"]))
		self.ui.lbl_wind_v.setText(f"{wind_speed} м/с")

		self.ui.lbl_wind_deg.setText(weather.wind_direction(weather_info["wind"]["deg"]))
		self.change_style(weather_info)

		icon = QIcon(weather.svg_to_pixmap("roll_up.svg", int(temp)))
		self.ui.btn_roll_up.setIcon(icon)

		self.set_info(weather_info)

	def set_info(self, weather_info):
		days_list = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
		def set_temp_text(temp, lbl):
			if round(temp) > 0:
				lbl.setText(f"+{round(temp)}")
			else:
				lbl.setText(f"{round(temp)}")
		def set_info_day(id_day, day, day_data):
			getattr(self.ui, f"lbl_date_{id_day}").setText(days_list[day])

			btn = getattr(self.ui, f"btn_date_{id_day}")
			icon = QIcon(weather.weather_icon(day_data["weather"][0]["id"], weather_info["main"]["temp_min"]))
			btn.setIcon(icon)

			set_temp_text(day_data["main"]["temp_min"],
						  getattr(self.ui, f"min_temp_date_{id_day}"))
			set_temp_text(day_data["main"]["temp_max"],
						  getattr(self.ui, f"max_temp_date_{id_day}"))
		weekday = datetime.now().weekday()
		set_info_day(1, weekday, self.mainw.weather_info["now"])
		for i in range(1, 7):
			day = weekday + i
			if day > 6:
				day -= 7
			set_info_day(i + 1, day, self.mainw.weather_info["daily"][day])

	def change_style(self, weather_info):
		temp = weather_info["main"]["temp_min"]
		
		bg_color_dict = rgb.get_bg_temperature_dict(temp)
		fg_color_dict = rgb.get_fg_temperature_dict(temp)
		bg_color = rgb.get_bg_temperature(temp)
		fg_color = rgb.get_fg_temperature(temp)

		self.ui.setStyleSheet(f"background: {bg_color};")
		lbl_text_qss = f"background: rgba(255,255,255,0);color: {fg_color};"
		for i in self.lbl_list:
			i.setStyleSheet(lbl_text_qss)

		btn_qss_bg = rgba.make_with_check(bg_color_dict["r"] - 25,
										 bg_color_dict["g"] - 25,
										 bg_color_dict["b"] - 25,
										 50)
		btn_qss_bg_pressed = rgba.make_with_check(bg_color_dict["r"] - 25,
												  bg_color_dict["g"] - 25,
												  bg_color_dict["b"] - 25,
												  255)
		btn_qss_bg_hover = rgba.make_with_check(bg_color_dict["r"] - 25,
												bg_color_dict["g"] - 25,
												bg_color_dict["b"] - 25,
												150)
		btn_qss = "QPushButton {"\
							f"background: {btn_qss_bg};"\
							f"border: 2px solid {fg_color};"\
					"} QPushButton:hover {"\
							f"background: {btn_qss_bg_hover};"\
					"} QPushButton:pressed {"\
							f"background: {btn_qss_bg_pressed};"\
					"}"
		for i in range(7):
			getattr(self.ui, f"btn_date_{i + 1}").setStyleSheet(btn_qss)
		self.ui.btn_roll_up.setStyleSheet(btn_qss)

	def choose_day_1(self):
		self.update_info(self.mainw.weather_info["now"])
		self.mainw.date_thread.change_lbl(self.ui.lbl_time)

	def _choose_day(self, dt, num):
		weekday = dt.weekday() + num
		if weekday > 6:
			weekday -= 7
		daily_info = self.mainw.weather_info["daily"][weekday]
		self.update_info(daily_info)
		self.mainw.date_thread.change_lbl(None)

		weekday = Count_Date.weekday_list[weekday]
		month = Count_Date.month_list[dt.month - 1]
		day = str(dt.day)
		dt = datetime.utcfromtimestamp(daily_info["dt"])
		time = dt.strftime("%H:%M:%S")
		date_str = f"{day} {month}, {weekday} {time}"
		self.ui.lbl_time.setText(date_str)

	def choose_day_2(self):
		self._choose_day(datetime.now(), 1)

	def choose_day_3(self):
		self._choose_day(datetime.now(), 2)

	def choose_day_4(self):
		self._choose_day(datetime.now(), 3)

	def choose_day_5(self):
		self._choose_day(datetime.now(), 4)

	def choose_day_6(self):
		self._choose_day(datetime.now(), 5)

	def choose_day_7(self):
		self._choose_day(datetime.now(), 6)

	def closeEvent(self, event):
		event.ignore()
		self.min_wnd.tray_icon.show()
		self.ui.hide()