"""Convert CSV format from money to Zaim format."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import _csv  # noqa: F401,RUF100


class Filter:
    """Base class for filtering lines from money.csv."""

    def process(self, line: list[str]) -> bool:
        """Check if the line contains the specified account."""
        raise NotImplementedError


class AccountFilter(Filter):
    def __init__(self, account: str) -> None:
        self.account = account

    def process(self, line: list[str]) -> bool:
        """Check if the line contains the specified account."""
        return self.account in (line[6], line[7])


class CsvLineStream:
    """Class to filter money.csv for specified accounts."""

    def __init__(self, input_csv: Path, output_csv: Path, flt: Filter) -> None:
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.filter = flt

    def start(self) -> None:
        """Read and filters money.csv only specified accounts."""
        with self.output_csv.open("w", encoding="utf-8") as file:
            self._start(csv.writer(file))

    def _start(self, writer: _csv._writer) -> None:
        """Filter lines from input_csv where specified accounts are present."""
        with self.input_csv.open("r", encoding="utf-8") as file:
            self.__start(csv.reader(file), writer)

    def __start(self, reader: _csv._reader, writer: _csv._writer) -> None:
        for line in (line for line in reader if self.filter.process(line)):
            writer.writerow(line)


def main() -> None:
    """Read and filters money.csv only specified accounts."""
    flt = AccountFilter(sys.argv[1])
    CsvLineStream(Path("money.csv"), Path("filtered_money.csv"), flt).start()


if __name__ == "__main__":
    main()
