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
        self.history = None

    def run(self, process: Process =None):
        if process is None:
            self.history.append("free")
            return
        if self.get_time() < process.arrival_time:
            self.wait(process.arrival_time - self.get_time())
        self.history.append(process.pid)

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

    def run_from_start(self):
        self.cpu.boot()
        clock = 0
        while len(self.process_pool) > 0:
            next_process = self.next_coming_process()
            while clock < next_process.arrival_time:
                clock += 1
                self.cpu.run(self.scheduler.next_to_run())
            self.scheduler.new_process(copy.copy(next_process))
            heapq.heappop(self.process_pool)

        while not self.scheduler.is_finished():
            self.cpu.run(self.scheduler.next_to_run())

        self.cpu.run(None)
        print(self.cpu.history)
        self.cpu.shutdown()
