import requests

def check_connection():
	timeout = 5
	try:
		request = requests.get("https://www.google.com", timeout=timeout)
		return True
	except (requests.ConnectionError, requests.Timeout) as exception:
		return False