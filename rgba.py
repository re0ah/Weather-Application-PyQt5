def check(r, g, b, a):
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
	if a > 255:
		a = 255
	elif a < 0:
		a = 0
	return r, g, b, a

def make(r, g, b, a):
	return f"rgba({r},{g},{b},{a})"

def make_with_check(r, g, b, a):
	r, g, b, a = check(r, g, b, a)
	return f"rgba({r},{g},{b},{a})"