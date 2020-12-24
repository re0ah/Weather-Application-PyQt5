from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QAction, QMenu, QSystemTrayIcon
import weather
from maximize import Maximize_window
import rgb
import rgba

class Minimize_window(QWidget):
	def __init__(self, app, mainw):
		self.app = app
		self.mainw = mainw
		super().__init__(None, Qt.WindowFlags())
		self.init_window()
		self.update_info()
		self.init_tray()

	def init_window(self):
		self.ui = uic.loadUi("minimize.ui")
		self.ui.btn_maximize.clicked.connect(self.maximize)
		self.ui.btn_roll_up.clicked.connect(self.roll_up)

		self.lbl_list = [self.ui.lbl_city, self.ui.lbl_weather_desc, self.ui.lbl_time,
						 self.ui.lbl_ctemp, self.ui.lbl_ctemp_feel, self.ui.lbl_temp,
						 self.ui.lbl_temp_feel, self.ui.lbl_cwind_v, self.ui.lbl_wind_deg,
						 self.ui.lbl_wind_v]


	def init_tray(self):
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon("tray_icon.png"))
		show_action = QAction("Показать", self)
		quit_action = QAction("Закрыть", self)
		show_action.triggered.connect(self.show_wnd)
		quit_action.triggered.connect(self.app.quit)
		tray_menu = QMenu()
		tray_menu.addAction(show_action)
		tray_menu.addAction(quit_action)
		self.tray_icon.setContextMenu(tray_menu)
		self.tray_icon.activated.connect(self.show_wnd_tray_activated)

	def show_wnd(self):
		self.mainw.show()
		self.tray_icon.hide()
		self.mainw.date_thread.change_lbl(self.ui.lbl_time)

	def show_wnd_tray_activated(self, state):
		if state == QSystemTrayIcon.Trigger: #left click
			self.mainw.show()
			self.tray_icon.hide()
			self.mainw.date_thread.change_lbl(self.ui.lbl_time)

	def roll_up(self):
		self.tray_icon.show()
		self.mainw.hide()

	def maximize(self):
		self.mainw.hide()
		self.max_wnd = Maximize_window(self.app, self.mainw, self)
		self.mainw.date_thread.change_lbl(self.max_wnd.ui.lbl_time)

	def update_info(self):
		weather_info = self.mainw.weather_info["now"]
		weather_desc = weather_info["weather"][0]["description"].capitalize()
		self.ui.lbl_weather_desc.setText(weather_desc)

		self.ui.lbl_city.setText(f"г. {weather_info['name']}")
		
		temp = str(round(weather_info["main"]["temp_min"]))
		self.ui.lbl_temp.setText(f"{temp}°C")

		temp_feel = str(round(weather_info["main"]["feels_like"]))
		self.ui.lbl_temp_feel.setText(f"{temp_feel}°C")

		weather_icon = weather.weather_icon(weather_info["weather"][0]["id"], int(temp))
		self.ui.lbl_weather_icon.setPixmap(weather_icon)

		wind_speed = str(weather_info["wind"]["speed"])
		self.ui.lbl_wind_v.setText(f"{wind_speed} м/с")

		self.ui.lbl_wind_deg.setText(weather.wind_direction(weather_info["wind"]["deg"]))

		icon = QIcon(weather.svg_to_pixmap("roll_up.svg", int(temp)))
		self.ui.btn_roll_up.setIcon(icon)

		icon = QIcon(weather.svg_to_pixmap("maximize.svg", int(temp)))
		self.ui.btn_maximize.setIcon(icon)

		self.change_style()

	def change_style(self):
		temp = self.mainw.weather_info["now"]["main"]["temp_min"]
		
		bg_color = rgb.get_bg_temperature(temp)
		fg_color = rgb.get_fg_temperature(temp)

		self.ui.setStyleSheet(f"background: {bg_color};")
		lbl_text_qss = f"background: rgba(255,255,255,0);color: {fg_color};"
		for i in self.lbl_list:
			i.setStyleSheet(lbl_text_qss)

		bg_color_dict = rgb.get_bg_temperature_dict(temp)
		fg_color_dict = rgb.get_fg_temperature_dict(temp)
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
		self.ui.btn_roll_up.setStyleSheet(btn_qss)
		self.ui.btn_maximize.setStyleSheet(btn_qss)