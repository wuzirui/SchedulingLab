import queue


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


class OS:
    cpu = Processor()
    scheduler = None
    process_pool = None

    def boot(self, scheduler):
        self.cpu.boot()
        self.scheduler = scheduler
        pass
