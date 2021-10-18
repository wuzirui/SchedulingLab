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

    def is_running(self):
        return self.history is not None

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

    def load_process(self, process):  # 所有process加入待处理字典
        if not self.process_dict.get(process.pid) is None:
            raise KeyError("Duplicate PID")
        heapq.heappush(self.process_pool, [process.arrival_time + 0.0000001 * self.get_process_num(), process])
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
            if process.arrival_time == clock:  # 判断是否有已经就绪者，加入就绪
                self.scheduler.new_process(copy.copy(process))
        next_pid = self.scheduler.next_to_run()
        if next_pid >= 0:
            next_process = self.process_dict[next_pid]
            assert next_process.remain_time > 0
            self.cpu_busy += self.cpu.run(next_process)
            next_process.remain_time -= 1
            next_process.history[-1] = "run"
            if next_process.remain_time == 0:
                self.scheduler.process_done(next_pid)
                next_process.finish_time = clock
                next_process.total_wait = clock - next_process.arrival_time - next_process.process_time + 1
                next_process.turn_around = next_process.total_wait + next_process.process_time
        else:
            self.cpu.wait(1)

    def run_from_start(self, print_history=True):
        if self.cpu.is_running():
            self.cpu.shutdown()
        self.cpu.boot()
        self._init_processes()
        self.clock = 0
        while self.cpu_busy < self.total_process_time:
            self._time_pulse(self.clock)
            self.clock += 1  # 每一次都要加一然后进入time_pulse
        if print_history:
            self.print_history(self.cpu.history)
        self.print_statistic()
        return self.cpu.history

    def print_history(self, cpu_his):
        print("Process History in Detail")
        print("-" * (20 + len(self.process_pool) * 10))
        print("%6s%10s" % ("clock", "CPU"), end="")
        for _, process in self.process_pool:
            print("%10s" % process.pid, end="")
        else:
            print("")
        for clock in range(self.clock):
            print("%4d" % clock, end='  ')
            print("%10s" % cpu_his[clock], end="")
            for _, process in self.process_pool:
                print("%10s" % process.history[clock], end="")
            else:
                print("")
        else:
            print("")

    def _print_attr_foreach_process(self, title: str, attr: str):
        print("%15s" % title, end="")
        for _, process in self.process_pool:
            print("%10s" % process.__getattribute__(attr), end="")
        else:
            print("")

    def _print_single_stat(self, title: str, data: float):
        print("%15s%10f" % (title, data))

    def print_statistic(self):
        print("Process Statistics in Detail")
        print("-" * (20 + len(self.process_pool) * 10))
        self._print_attr_foreach_process("stat", "pid")
        self._print_attr_foreach_process("arrival time", "arrival_time")
        self._print_attr_foreach_process("process time", "process_time")
        self._print_attr_foreach_process("total wait", "total_wait")
        self._print_attr_foreach_process("turn around", "turn_around")

        self._print_single_stat("avg wait", self.get_avg_wait())
        self._print_single_stat("avg turn around", self.get_avg_turn_around())

    def get_total_wait(self):
        total_wait = 0
        for _, process in self.process_pool:
            total_wait += process.total_wait
        return total_wait

    def get_process_num(self):
        return len(self.process_pool)

    def get_avg_wait(self):
        return self.get_total_wait() / self.get_process_num()

    def get_avg_turn_around(self):
        total_turn_around= 0
        for _, process in self.process_pool:
            total_turn_around += process.total_wait + process.process_time
        return total_turn_around / self.get_process_num()


