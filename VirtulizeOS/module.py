from Schedulers import module
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

    def run(self, process=None):
        if process is not None:
            self.history.append(process)
            return
        self.history.append("free")

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

    def __init__(self, scheduler: module):
        self.scheduler = scheduler
        self.process_pool = []
        pass

    def load_processes(self, processes):
        for process in processes:
            heapq.heappush(self.process_pool, [process.arrival_time, process])

    def load_process(self, process):
        heapq.heappush(self.process_pool, [process.arrival_time, process])

    def size_of_pool(self):
        return len(self.process_pool)

    def next_coming_process(self):
        return self.process_pool[0][1]

    def run_from_start(self):
        self.cpu.boot()
        clock = 0
        while len(self.process_pool) > 0:
            self.cpu.run(self.next_coming_process())
            heapq.heappushpop(self.next_coming_process())
        self.cpu.run(None)
        self.cpu.shutdown()
