from VirtulizeOS.process import Process
from .module import AbstractScheduler
from collections import deque


class SRTFScheduler(AbstractScheduler):
    processes = []

    def next_to_run(self) -> int:
        if len(self.processes) == 0:
            return -1
        self.processes = sorted(self.processes, key=lambda process: process.process_time, reverse=False)
        return self.processes[0].pid

    def new_process(self, process: Process):
        self.processes.append(process)

    def process_done(self, pid: int):
        assert len(self.processes) > 0, "no process in queue"
        assert self.processes.pop(0).pid == pid
