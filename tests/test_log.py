import unittest

from core.log import log, logger


class TestLogFunction(unittest.TestCase):
    def test_log_function(self):
        with self.assertLogs(logger, level="INFO") as l:
            log(level="info", message="Info Level Test Case.")
        self.assertEqual(len(l.output), 1)
        self.assertIn("INFO:core.log:Info Level Test Case.", l.output[0])

        with self.assertLogs(logger, level="WARNING") as l:
            log(level="warning", message="Warning Level Test Case.")
        self.assertEqual(len(l.output), 1)
        self.assertIn("WARNING:core.log:Warning Level Test Case.", l.output[0])

        with self.assertLogs(logger, level="ERROR") as l:
            log(level="error", message="Error Level Test Case.")
        self.assertEqual(len(l.output), 1)
        self.assertIn("ERROR:core.log:Error Level Test Case.", l.output[0])


if __name__ == "__main__":
    unittest.main()
