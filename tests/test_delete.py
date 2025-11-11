import unittest
import tempfile

from pathlib import Path
from utils.search_duplicate import delete_duplicates


class TestDeleteFunction(unittest.TestCase):
    def test_delete_function(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".tmp", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            src_file = Path(temp.name)

        try:
            delete_duplicates(duplicate_files=[src_file])
            self.assertFalse(src_file.exists())

        finally:
            if src_file.exists():
                src_file.unlink()


if __name__ == "__main__":
    unittest.main()
