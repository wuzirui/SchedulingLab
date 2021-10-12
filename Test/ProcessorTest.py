import unittest
from VirtulizeOS.module import Processor


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


if __name__ == '__main__':
    unittest.main()
