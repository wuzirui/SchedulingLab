from VirtulizeOS.process import Process
from .module import AbstractScheduler
from collections import deque


class FIFSScheduler(AbstractScheduler):
    processes = deque()

    def next_to_run(self) -> int:
        if len(self.processes) == 0:
            return -1
        return self.processes[0].pid

    def new_process(self, process: Process):
        self.processes.append(process)

    def process_done(self, pid: int):
        assert len(self.processes) > 0, "no process in queue"
        assert self.processes.popleft().pid == pid
