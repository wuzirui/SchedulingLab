import copy

from Schedulers import module
from .process import Process
import heapq


class Processor:
    history = None

    def __init__(self):
        pass

    def boot(self):
        assert self.history is None, "already booted, shutdown() first"
        self.history = []
        pass

    def shutdown(self):
        assert self.history is not None, "processor not running, use boot() first"
        ret = self.history
        self.history = None
        return ret

    def run(self, process: Process = None):
        if process is None:
            self.history.append("free")
            return 0
        assert self.get_time() >= process.arrival_time, f"current time = {self.get_time()}, but process{process.pid} arrives at {process.arrival_time}"
        self.history.append(process.pid)
        return 1

    def get_time(self):
        assert self.history is not None, "processor not running, use boot() first"
        return len(self.history)

    def wait(self, time: int):
        assert self.history is not None, "processor not running, use boot() first"
        assert time > 0, "input invalid"
        self.history.extend(["free"] * time)


class VirtualOS:
    cpu = Processor()
    scheduler = None
    process_pool = None
    process_dict = None
    total_process_time = 0
    cpu_busy = 0
    clock = 0

    def __init__(self, scheduler: module):
        self.scheduler = scheduler
        self.process_pool = []
        self.process_dict = {}
        pass

    def load_processes(self, processes):
        for process in processes:
            self.load_process(process)

    def load_process(self, process):
        if not self.process_dict.get(process.pid) is None:
            raise KeyError("Duplicate PID")
        heapq.heappush(self.process_pool, [process.arrival_time, process])
        self.process_dict[process.pid] = process

    def size_of_pool(self):
        return len(self.process_pool)

    def next_coming_process(self):
        return self.process_pool[0][1]

    def _init_processes(self):
        for _, process in self.process_pool:
            process.remain_time = process.process_time
            self.total_process_time += process.process_time
            process.status = "undefined"
            process.history = []

    def _time_pulse(self, clock):
        for _, process in self.process_pool:
            process.history.append("ready" if process.arrival_time <= clock else "undefined")
            if process.remain_time == 0:
                process.history[-1] = "Done"
            if process.arrival_time == clock:
                self.scheduler.new_process(copy.copy(process))
        if (next_pid := self.scheduler.next_to_run()) >= 0:
            next_process = self.process_dict[next_pid]
            assert next_process.remain_time > 0
            self.cpu_busy += self.cpu.run(next_process)
            next_process.remain_time -= 1
            if next_process.remain_time == 0:
                self.scheduler.process_done(next_pid)
            next_process.history[-1] = "run"
        else:
            self.cpu.wait(1)

    def run_from_start(self):
        self.cpu.boot()
        self._init_processes()
        self.clock = 0
        while self.cpu_busy < self.total_process_time:
            self._time_pulse(self.clock)
            self.clock += 1
        self.print_history()
        self.print_statistic()
        return self.cpu.shutdown()

    def print_history(self):
        print(list(range(self.clock)))
        for _, process in self.process_pool:
            print(process.history)

    def print_statistic(self):
        pass

