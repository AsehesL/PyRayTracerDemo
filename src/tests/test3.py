from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue

a = ProcessPoolExecutor()

print(dir(a))

print(a._max_workers)

b = Queue()

print(dir(b))

print(b.empty())

b.put(2)

print(b.empty())