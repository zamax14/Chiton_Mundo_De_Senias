import sys

nombre = sys.argv[1]
print("hola mundo")

def test(name):
	print("hola"+name)
	return True

test(nombre)
