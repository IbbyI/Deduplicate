import unittest
import tempfile
from pathlib import Path

from core.actions import move_duplicates


class TestMoveFunction(unittest.TestCase):
    def test_move_function(self):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".tmp", delete=False
        ) as temp:
            temp.write("Test Case.")
            temp.flush()
            src_file = Path(temp.name)

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_dir = Path(tmpdir)

            move_duplicates(
                duplicate_files=[src_file], move_path=dest_dir, dry_run_flag=False
            )

            dest = dest_dir / src_file.name

            self.assertFalse(src_file.exists())
            self.assertTrue(dest.exists())

            if dest.exists():
                dest.unlink()


if __name__ == "__main__":
    unittest.main()
