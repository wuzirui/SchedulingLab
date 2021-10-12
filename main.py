from VirtulizeOS.module import VirtualOS
from VirtulizeOS.process import Process
from Schedulers.FIFS import FIFSScheduler

if __name__ == "__main__":
    process1 = Process(1, 1, 10)
    process2 = Process(2, 2, 1)
    process3 = Process(3, 0, 5)
    os = VirtualOS(FIFSScheduler())
    os.load_processes([process1, process2, process3])
    os.run_from_start()


