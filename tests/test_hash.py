import unittest
import tempfile
from pathlib import Path

from utils.hash import hash_file


class TestHashFunction(unittest.TestCase):
    def test_hash_function(self):
        hash_fn = hash_file
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            results = hash_fn(Path(temp.name))

        self.assertIsInstance(results.strip(), str)
        self.assertEqual(len(results.strip()), 64)
        self.assertRegex(results.strip(), r"^[a-fA-F0-9]{64}$")


if __name__ == "__main__":
    unittest.main()
