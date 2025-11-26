import unittest
import tempfile
from os import urandom
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch

from core.hasher import auto_hash, full_hash, quick_hash

TEST_STRING = "Test Case"


class TestHashFunction(unittest.TestCase):
    @patch("test_hash.auto_hash")
    def test_auto_hash_function(self, mock_auto_hash):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write(str(urandom(7000)))
            temp.flush()

        auto_hash_results = auto_hash(Path(temp.name)).strip()
        mock_auto_hash.assert_called_once()

    def test_quick_hash_function(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write(str(urandom(8500)))
            temp.flush()

        quick_hash_results = quick_hash(Path(temp.name)).strip()
        full_hash_results = full_hash(Path(temp.name)).strip()

        self.assertIsInstance(quick_hash_results, str)
        self.assertEqual(len(quick_hash_results), 64)
        self.assertRegex(quick_hash_results, r"^[a-fA-F0-9]{64}$")
        self.assertNotEqual(quick_hash_results, full_hash_results)

    def test_full_hash_function(self):
        sha256_hash = sha256()
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as temp:
            temp.write(TEST_STRING)
            temp.flush()

        file_hash_results = full_hash(Path(temp.name)).strip()
        sha256_hash.update(bytes(TEST_STRING, encoding="utf-8"))
        hash_results = sha256_hash.hexdigest().strip()

        self.assertEqual(file_hash_results, hash_results)
        self.assertIsInstance(file_hash_results, str)
        self.assertEqual(len(file_hash_results), 64)
        self.assertRegex(file_hash_results, r"^[a-fA-F0-9]{64}$")


if __name__ == "__main__":
    unittest.main()
