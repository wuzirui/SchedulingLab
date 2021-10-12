from VirtulizeOS.process import Process
from .module import AbstractScheduler
from collections import deque


class FIFSScheduler(AbstractScheduler):
    processes = deque()
    finish_time_dict = {}

    def next_to_run(self):
        if len(self.processes) == 0:
            return None
        ret = self.processes[0]
        ret.remain_time -= 1
        if ret.remain_time == 0:
            self.processes.popleft()
        return ret

    def new_process(self, process: Process):
        assert process.process_time > 0
        process.remain_time = process.process_time
        self.processes.append(process)

    def is_finished(self):
        return self.processes is None or len(self.processes) == 0
