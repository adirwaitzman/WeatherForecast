import unittest
import os
import requests
from time import sleep


class TestConnection(unittest.TestCase):

    def setUp(self):
        # Create a test client
        os.popen("docker run -d -p 9090:8000 --name app-test_connection weatherapp:latest")
        sleep(5)

    def tearDown(self):
        os.popen("docker rm -f app-test_connection")

    def test_Connection(self):
        # Use the test client to simulate a request
        self.response = requests.get("http://127.0.0.1:9090")
        self.assertEqual(self.response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
