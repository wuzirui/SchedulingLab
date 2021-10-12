from VirtulizeOS.process import Process
from module import AbstractScheduler
import queue


class FIFSScheduler(AbstractScheduler):
    processes = queue.Queue()

    def next_to_run(self):
        if self.processes.qsize() == 0:
            return None
        return self.processes.get()

    def new_process(self, process: Process):
        self.processes.append(process)
