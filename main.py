from VirtulizeOS.module import VirtualOS
from VirtulizeOS.process import Process
from Schedulers.FIFS import FIFSScheduler

if __name__ == "__main__":
    process1 = Process(1, 0, 7)
    process2 = Process(2, 2, 4)
    process3 = Process(3, 4, 1)
    process4 = Process(4, 5, 4)
    os = VirtualOS(FIFSScheduler())
    os.load_processes([process1, process2, process3, process4])
    os.run_from_start()
