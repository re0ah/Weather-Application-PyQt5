from PyQt5.QtCore import QThread
import datetime

class Count_Date(QThread):
	"""class for changing text in QLabel per sec"""
	def __init__(self, lbl_time):
		""""set QLabel what will changing and create datetime what
		will increment by 1 sec per 1 sec"""
		self.lbl_time = lbl_time
		super().__init__(None)
		self.dt = datetime.datetime.now()

	def run(self):
		while 1:
			self.update()
			self.sleep(1)
			self.dt += datetime.timedelta(seconds=1)

	weekday_list = ["Понедельник",	#0
					"Вторник",		#1
					"Среда",		#2
					"Четверг",		#3
					"Пятница",		#4
					"Суббота",		#5
					"Воскресенье"]	#6
	month_list = ["Января",		#0
				  "Февраля",	#1
				  "Марта",		#2
				  "Апреля",		#3
				  "Мая",		#4
				  "Июня",		#5
				  "Июля",		#6
				  "Августа",	#7
				  "Сентября",	#8
				  "Октября",	#9
				  "Ноября",		#10
				  "Декабря"]	#11
	def update(self):
		if self.lbl_time == None:
			return
		"""make string by format and set text in QLabel"""
		weekday = self.weekday_list[self.dt.weekday()]
		month = self.month_list[self.dt.month - 1]
		day = str(self.dt.day)
		time = self.dt.strftime("%H:%M:%S")
		date_str = f"{day} {month}, {weekday} {time}"
		self.lbl_time.setText(date_str)

	def change_lbl(self, lbl):
		"""change QLable what been changing and update him"""
		self.lbl_time = lbl
		self.update()