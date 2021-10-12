from abc import ABC, abstractmethod
from VirtulizeOS.process import Process


class AbstractScheduler(ABC):

    @abstractmethod
    def next_to_run(self):
        pass

    @abstractmethod
    def new_process(self, process: Process):
        pass

    @abstractmethod
    def is_finished(self):
        pass

