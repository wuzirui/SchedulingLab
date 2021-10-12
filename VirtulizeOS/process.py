class Process:
    pid = 0
    arrival_time = 0
    process_time = 0

    def __init__(self, pid, arrival_time, process_time):
        self.pid, self.arrival_time, self.process_time = pid, arrival_time, process_time

