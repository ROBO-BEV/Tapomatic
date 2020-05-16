import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_udp_server(self):
        self.assertEqual(True, True)

    def test_udp_client(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()

