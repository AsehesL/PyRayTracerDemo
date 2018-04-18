from multiprocessing import Process, Queue, Manager, SimpleQueue
import random
from time import sleep
from concurrent.futures import ProcessPoolExecutor


def run_task(pid, taskqueue, resultqueue):
	while taskqueue.empty() == False:
		task = taskqueue.get()
		print("Processing Task...   PID:%d, data%d"%(pid, task))
		sleep(1)
		result = task * 2
		resultqueue.put_nowait(result)


if __name__ == "__main__":
	tskqueue = Queue()
	rqueue = Queue()

	tasks = []

	for j in range(0, 100):
		tskqueue.put(random.randint(0,600))

	for i in range(0, 8):
		pw = Process(target = run_task, args=(i, tskqueue, rqueue))
		tasks.append(pw)

	for task in tasks:
		print("Run Task")
		task.start()
		#task.join()

	runpc = 0
	while runpc < 100:
		if rqueue.empty() == False:
			rst = rqueue.get_nowait()
			print(rst)
			runpc += 1
