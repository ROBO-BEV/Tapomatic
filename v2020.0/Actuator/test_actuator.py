import unittest
import Actuator
import Motor
import Relay

class TestActuator(unittest.TestCase):
    def test_sample(self):
        m = Motor(1,1234,'FWD')
        self.assertIsInstance(Actuator)

if __name__ == '__main__':
    unittest.main(verbosity=2)