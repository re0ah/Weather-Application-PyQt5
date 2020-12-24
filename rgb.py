def check(r, g, b):
	if r > 255:
		r = 255
	elif r < 0:
		r = 0
	if g > 255:
		g = 255
	elif g < 0:
		g = 0
	if b > 255:
		b = 255
	elif b < 0:
		b = 0
	return r, g, b

def make(r, g, b):
	return f"rgb({r},{g},{b})"

def make_with_check(r, g, b):
	r, g, b = check(r, g, b)
	return f"rgb({r},{g},{b})"

def get_bg_temperature(temp):
	rgb_dict = get_bg_temperature_dict(temp)
	return make(rgb_dict['r'], rgb_dict['g'], rgb_dict['b'])

def get_bg_temperature_dict(temp):
	bg_r = 255
	bg_g = 60
	bg_b = 0
	if temp < 30:
		if temp < 0:
			t = 30 + int(abs(temp))
		else:
			t = 30 - int(abs(temp))
		if temp >= 15:
			bg_g += int(t * 12)
		elif (temp >= 0) & (temp < 15):
			bg_r = 100 + (t * 5)
			bg_g = 100 + (t * 4)
			bg_b = int(t * 8)
		elif (temp >= -25) & (temp < 0):
			bg_r = 10
			bg_g = 10 + t
			bg_b = int(t * 4.25)
		elif (temp <= -25):
			bg_r = 0
			bg_g = 30
			bg_b = 170
	return {"r": bg_r, "g": bg_g, "b": bg_b}

def get_fg_temperature(temp):
	rgb_dict = get_fg_temperature_dict(temp)
	return make(rgb_dict['r'], rgb_dict['g'], rgb_dict['b'])

def get_fg_temperature_dict(temp):
	fg_r = 0
	fg_g = 0
	fg_b = 0
	if temp < 30:
		if temp < 0:
			t = 30 + int(abs(temp))
		else:
			t = 30 - int(abs(temp))
		if (temp >= -10) & (temp < 0):
			fg_r += int(t * 6.25)
			fg_g += int(t * 6.25)
			fg_b += int(t * 6.25)
		elif temp <= -10:
			fg_r = 255
			fg_g = 255
			fg_b = 255
	return {"r": fg_r, "g": fg_g, "b": fg_b}