import unittest

from core.log import log


class TestLogFunction(unittest.TestCase):
    def test_log_function(self):
        self.assertLogs(log(level="info", message="Info Level Test Case."))
        self.assertLogs(log(level="warning", message="Warning Level Test Case."))
        self.assertLogs(log(level="error", message="Error Level Test Case."))


if __name__ == "__main__":
    unittest.main()
