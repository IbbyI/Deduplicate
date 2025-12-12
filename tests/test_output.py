import csv
import sqlite3
import unittest
import tempfile

from pathlib import Path
from os.path import exists
from tabulate import tabulate

from core.output import write_csv_output, write_db_output, write_txt_output
from ui.adapter_output import OUTPUT_FILE_HEADERS

TEST_DATA = [
    "/.tmp",
    "2 bytes",
    "Created: 29/11/2025 23:21:53",
    "Last Modified: 29/11/2025 23:21:53",
]


class TestOutputFunction(unittest.TestCase):
    def test_txt_file_output(self):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as temp:
            table = tabulate(TEST_DATA, headers=OUTPUT_FILE_HEADERS, missingval="N/A")
            write_txt_output(
                TEST_DATA, output_file=Path(temp.name), file_headers=OUTPUT_FILE_HEADERS
            )
            temp_file_contents = temp.read()
        self.assertEqual(temp_file_contents, table)

    def test_csv_file_output(self):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as temp:
            write_csv_output(
                [TEST_DATA],
                output_file=Path(temp.name),
                file_headers=OUTPUT_FILE_HEADERS,
            )
            temp.seek(0)
            reader = list(csv.reader(temp, dialect="excel"))
        expected = [OUTPUT_FILE_HEADERS, TEST_DATA]
        self.assertEqual(reader, expected)

    def test_db_file_output(self):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".db", delete=False) as temp:
            write_db_output([TEST_DATA], Path(temp.name))

            with sqlite3.connect(temp.name) as con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM deduplicate")
                db_results = cursor.fetchall()
                with self.assertRaises(sqlite3.OperationalError):
                    cursor.execute("CREATE TABLE deduplicate")
            assert exists(temp.name)
            self.assertEqual(list(db_results[0])[1:], TEST_DATA)


if __name__ == "__main__":
    unittest.main()
