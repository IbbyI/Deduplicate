import unittest
import tempfile
from pathlib import Path

from core.scanner import find_duplicates
from core.hasher import auto_hash


class TestFileFunction(unittest.TestCase):
    def test_find_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = Path(tmpdir)
            subdir = Path(tempfile.mkdtemp(dir=tmpdir))
            ignored_file = tempfile.TemporaryFile(dir=subdir)
            for i in range(2):
                with tempfile.NamedTemporaryFile(
                    mode="w+", suffix=".tmp", delete=False, dir=src_dir
                ) as temp:
                    temp.write("Test Case.")
                    temp.flush()
            dupe_files = find_duplicates(
                start_path=src_dir,
                ignore_path=subdir,
                hash_func=auto_hash,
                update_progress=None,
            )
            if dupe_files:
                self.assertTrue(type(dupe_files), list[list[Path]])
                self.assertNotIn(subdir, dupe_files)
                self.assertNotIn(ignored_file, dupe_files)
            else:
                self.fail("No Duplicate Files Found.")

            self.assertTrue(src_dir.exists())

        ignored_file.close()


if __name__ == "__main__":
    unittest.main()
