import unittest
from unittest.mock import Mock
from VirtulizeOS.module import *
from VirtulizeOS.process import Process
from Schedulers.module import AbstractScheduler


class ProcessorFunctionalTest(unittest.TestCase):
    def test_processor(self):
        cpu = Processor()
        cpu.boot()
        cpu.run()
        cpu.run("A")
        cpu.run()
        self.assertEqual(cpu.get_time(), 3)
        cpu.shutdown()
        self.assertIsNone(cpu.history)
        cpu.boot()
        self.assertEqual(cpu.get_time(), 0)


class VOSTest(unittest.TestCase):

    def test_can_load_processes(self):
        process1 = Process(1, 1, 10)
        process2 = Process(2, 2, 1)
        process3 = Process(3, 0, 5)

        os = VirtualOS(None)
        os.load_process(process1)
        self.assertEqual(os.next_coming_process().pid, 1)
        os.load_processes([process2, process3])
        self.assertEqual(os.size_of_pool(), 3)
        self.assertEqual(os.next_coming_process().pid, 3)


if __name__ == '__main__':
    unittest.main()
