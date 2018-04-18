from multiprocessing import Process, Queue, Manager, SimpleQueue
import random
from time import sleep
from concurrent.futures import ProcessPoolExecutor

def run_task(pid, queue, slist):
	while queue.empty() == False:
		dt = queue.get()
		#print("PID:%d, Data:%d"%(pid, dt))
		slist.append(dt*5)
		sleep(0.5)

def run_task2(pid):
	print("PID:%d"%(pid))


if __name__ == '__main__':
	

	with Manager() as manager:
		queue = Queue()
		sharelist = manager.list()

		#pool = Pool()
		#executor = ProcessPoolExecutor()

		for j in range(0, 100):
			queue.put(j)

		# for i in range(0, 8):
		# 	pool.apply(run_task, args = (i, queue))
		# pool.close()

		# taskResults = []
		# for i in range(0, executor._max_workers):
		# 	taskResults.append(executor.submit(run_task, i, queue))

		# for result in taskResults:
		# 	result.result()

		tasks = []
		for i in range(0, 1):
			pw = Process(target = run_task, args = (i, queue, sharelist))
			tasks.append(pw)

		for task in tasks:
			task.start()
			#task.join()

		for l in sharelist:
			print(l)

	#print(data)