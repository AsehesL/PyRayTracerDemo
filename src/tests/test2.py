from concurrent.futures import ThreadPoolExecutor
import time
import threading

def test_func(a, b):
	mutes = threading.Lock()
	for i in range(0, a):
		b+=1
	time.sleep(3)
	mutes.release()
	return b

exctor = ThreadPoolExecutor(8)

ft1 = exctor.submit(test_func, 700000, 2)
ft2 = exctor.submit(test_func, 700, 3)

print(ft1.done())
print("x")

print(ft2.result())