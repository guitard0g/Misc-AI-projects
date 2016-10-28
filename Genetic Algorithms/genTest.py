def gen():
	for i in range(10):
		yield i

def main():
	for i in gen():
		print(i)
main()