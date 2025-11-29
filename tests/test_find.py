import unittest
import tempfile
from pathlib import Path

from core.scanner import find_duplicates
from core.hasher import auto_hash


class TestFileFunction(unittest.TestCase):
    def test_find_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir)
            for i in range(2):
                with tempfile.NamedTemporaryFile(
                    mode="w+", suffix=".tmp", delete=False, dir=src_dir
                ) as temp:
                    temp.write("Test Case.")
                    temp.flush()

            self.assertTrue(
                type(
                    find_duplicates(
                        start_path=src_dir, ignore_path=None, hash_func=auto_hash
                    )
                ),
                list[list[Path]],
            )
            self.assertTrue(src_dir.exists())

        if src_dir.exists():
            src_dir.unlink()


if __name__ == "__main__":
    unittest.main()
