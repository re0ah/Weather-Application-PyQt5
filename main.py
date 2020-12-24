from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
import weather
import location
import internet_connection
from minimize import Minimize_window
from count_date import Count_Date

class Mainw(QWidget):
	def __init__(self, app):
		self.app = app
		super().__init__(None, Qt.WindowFlags())
		self.check_connection()
		#set window style without borders, title bar and buttons
		self.setWindowFlags(Qt.FramelessWindowHint)

		self.update_weather_info()

		self.init_window()
		self.date_thread = Count_Date(None)
		self.date_thread.start()
		self.date_thread.change_lbl(self.min_wnd.ui.lbl_time)

	def init_window(self):
		screensize = self.app.desktop().availableGeometry()
		self.vbox = QVBoxLayout()
		self.min_wnd = Minimize_window(self.app, self)

		self.resize(self.min_wnd.ui.size())

		self.move(screensize.width() - self.min_wnd.ui.width(),
				  screensize.height() - self.min_wnd.ui.height())

		self.vbox.addWidget(self.min_wnd.ui)
		self.setLayout(self.vbox)
		self.vbox.setContentsMargins(0, 0, 0, 0)
		self.show()

	def update_weather_info(self):
		"""get current geoposition and make weather info for this location"""
		geodata = location.current_location()
		self.weather_info = weather.get(geodata["lat"], geodata["lon"])

	def check_connection(self):
		"""check if connection exist, if exist - do nothing, else show
			msgbox and close app"""
		if internet_connection.check_connection() == False:
			reply = QMessageBox.question(self,
									"Соединение с интернетом отсутствует",
									"Соединение с интернетом отсутствует",
									QMessageBox.Ok)
			self.app.quit()

if __name__ == "__main__":
	app = QApplication([])
	loginw = Mainw(app)
	app.exec_()