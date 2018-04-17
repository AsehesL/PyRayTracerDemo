from multiprocessing import Pool, Process, Queue
from concurrent.futures import ProcessPoolExecutor
import random
from time import sleep



def run_task(pid, q):
	print("pid:%d"%pid)
	# while q.empty() == False:
	# 	it = q.get()
	# 	print("PID:%d,Value:%d"%(pid, it))
	#it = queue.get()
	#print("PID:%d"%pid)
	#print("PID:%d,Value:%d"%(pid, it))

if __name__ == '__main__':
	#executor = ProcessPoolExecutor()
	queue = Queue()

	for j in range(0, 100):
		rd = random.randint(0,600)
		queue.put(j)

	#results = []

	#tasks = []
	pool = Pool()
	for i in range(0, 8):
	#for i in range(0, executor._max_workers):
		#results.append(executor.submit(run_task, i, queue))
		#pw = Process(target = run_task, args=(i, queue))
		#tasks.append(pw)
		result = pool.apply_async(run_task, (i,queue))

	#for task in tasks:
	#	task.start()
	pool.close()
	pool.join()

	if result.successful():
		print("All Done")

	#for result in results:
	#	result.result()