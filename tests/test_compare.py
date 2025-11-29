import unittest
import tempfile
from pathlib import Path

from core.comperator import compare_files


class TestCompareFunction(unittest.TestCase):
    def test_compare_function(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".tmp", delete=False
        ) as temp1:
            temp1.write("Test Case.")
            temp1.flush()
            src_file1 = Path(temp1.name)

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".tmp", delete=False
        ) as temp2:
            temp2.write("Test Case.")
            temp2.flush()
            src_file2 = Path(temp2.name)

        try:
            compare_list = [[src_file1, src_file2]]
            comparison = compare_files(duplicate_results=compare_list)

            self.assertTrue(src_file1.exists())
            self.assertTrue(src_file2.exists())

            self.assertIsInstance(comparison, list)
            self.assertEqual(len(comparison), 1)

            oldest = min([src_file1, src_file2], key=lambda f: f.stat().st_mtime)
            self.assertNotEqual(comparison[0], oldest)
        finally:
            if src_file1.exists():
                src_file1.unlink()
            if src_file2.exists():
                src_file2.unlink()


if __name__ == "__main__":
    unittest.main()
