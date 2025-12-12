from pathlib import Path
from os.path import splitext

from ui.display import success
from ui.verbose import verbose

from core.log import log
from core.output import (
    write_db_output,
    write_txt_output,
    write_csv_output,
    output_file_format,
)

ALLOWED_EXT = [".txt", ".csv", ".db", ".sqlite"]
DEFAULT_FILE_EXT = ".txt"
OUTPUT_FILE_HEADERS = ["Path", "File Size", "Created Date", "Last Modified Date"]


@verbose(
    lambda args, result: f"Output File Set as {args[1]}, Duplicate Files Passed: {True if args[0] else False}"
)
def handle_output_file(duplicate_files: list[Path], output_file: Path) -> None:
    """
    Handles UI to Write to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    try:
        file_extension = splitext(output_file)[1]
        if not file_extension:
            file_extension = DEFAULT_FILE_EXT
            output_file = Path(str(output_file) + file_extension)

        log(
            level="info",
            message=f"Output File Set To: {output_file}, File Extension: {file_extension}",
        )

        output_file_data = output_file_format(duplicate_files)
        if file_extension not in ALLOWED_EXT:
            raise ValueError(
                f"{file_extension} File Extension is not Supported For Output File."
            )
        if file_extension == ".csv":
            write_csv_output(output_file_data, output_file, OUTPUT_FILE_HEADERS)
        elif file_extension == ".txt":
            write_txt_output(output_file_data, output_file, OUTPUT_FILE_HEADERS)
        elif file_extension in {".db", ".sqlite"}:
            write_db_output(output_file_data, output_file)

        success(
            f"Sucessfully Wrote to Output File: {output_file}", style="bold underline"
        )
        log(level="info", message=f"Sucessfully Wrote to Output File: {output_file}")
    except IOError as e:
        log(
            level="error",
            message=f"❌ Failed To Write to Output File: {output_file}, {e}",
        )
        raise IOError(f"❌ Failed To Write to Output File: {output_file}, {e}") from e
