import unittest
from unittest.mock import patch
from UDPServer import *
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_udp_server(self):
        self.assertEqual(True, True)

    def test_udp_client(self):
        self.assertEqual(True, True)

    @patch('UDPServer.socket.socket')  # Patch the class
    def test_msearch(self, mock_socket):
        #TODO HAVE TO COMPLETE THE TEST CASE.
        mock_socket = mock_socket.return_value  # We want the instance
        obj = UDPServer()
        mock_socket.recvfrom.return_value = [0, '1']
        #mock_socket.recvfrom.side_effect = [0, '1']
        UDPServer.raspberryServerProgram(obj,'coco_orders.csv')
        mock_socket.settimeout.assert_called_with(2)
if __name__ == '__main__':
    unittest.main()

