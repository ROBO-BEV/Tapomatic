import unittest
import Actuator
from Motor import Motor

class TestActuator(unittest.TestCase):
    def test_sample(self):
        m = Motor([1,2],1234,'FWD')
        self.assertIsInstance(m, Actuator.Actuator)

if __name__ == '__main__':
    unittest.main(verbosity=2)