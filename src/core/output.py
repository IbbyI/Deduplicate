import os
import csv
import sqlite3
import datetime
import time
import logging
from tabulate import tabulate

from pathlib import Path


def output_file_format(duplicate_files: list[Path]) -> list[list[str]]:
    """
    Format Duplicate Files for Output File.
    Args:
        duplicate_files (list[Path]):  List of Duplicate Files Found.
    Returns:
        list[str]: Formatted Data to Write to Output File.
    """
    output_file_data = []
    for p in duplicate_files:
        dt_created = datetime.datetime.fromtimestamp(os.path.getctime(p)).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        dt_modified = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        file_size = f"{os.path.getsize(p)} bytes"
        created, last_modified = str(dt_created), str(dt_modified)

        output_file_data.append([str(p), file_size, created, last_modified])
    return output_file_data


def write_txt_output(
    output_file_data: list, output_file: Path, file_headers: list[str]
) -> None:
    table = tabulate(output_file_data, headers=file_headers, missingval="N/A")
    with open(output_file, "w") as f:
        f.write(table)


def write_csv_output(
    output_file_data: list[list[str]], output_file: Path, file_headers: list[str]
) -> None:
    with open(output_file, "w", newline="", encoding='utf-8') as f:
        csvwriter = csv.writer(f)

        csvwriter.writerow(file_headers)
        csvwriter.writerows(output_file_data)


def write_db_output(output_file_data: list[list[str]], output_file: Path) -> None:
    class DatabaseError(Exception):
        pass

    max_retries = 5
    base_delay = 0.1

    for attempt in range(1, max_retries + 1):
        try:
            with sqlite3.connect(str(output_file), timeout=30) as con:
                try:
                    con.execute("PRAGMA journal_mode=WAL;")
                except sqlite3.DatabaseError:
                    logging.debug("Could not set WAL journal mode.")

                cur = con.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS deduplicate(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        Path TEXT, 
                        File_Size TEXT, 
                        Created_Date TEXT, 
                        Last_Modified_Date TEXT
                    )"""
                )
                if output_file_data:
                    cur.executemany(
                        """
                        INSERT INTO deduplicate(
                            Path, File_Size, Created_Date, Last_Modified_Date) 
                            VALUES (?, ?, ?, ?)""",
                        output_file_data,
                    )
                cur.close()
            return
        except sqlite3.OperationalError as e:
            msg = str(e).lower()
            if "locked" in msg and attempt < max_retries:
                delay = base_delay * (2 ** (attempt - 1))
                logging.warning(
                    "Database is locked, retrying in %.2fs (attempt %d/%d)",
                    delay,
                    attempt,
                    max_retries,
                )
                time.sleep(delay)
                continue
            raise DatabaseError(f"Operational error writing DB: {e}") from e
        except sqlite3.Error as e:
            raise DatabaseError(f"SQLite error writing DB: {e}") from e
