import os.path
import re
from utilities.constants import Constants


class FileUtility:

    file_name: str
    regex = None

    def __init__(self, file_name: str):
        """
        Initialize variables and compiles regex pattern.

        Parameters
        ----------
        file_name: str
            The filename representing its full path.
        """
        self.file_name = file_name
        self.regex = re.compile(Constants.FULL_RECORD_REGEX)

    def check_file_exists(self) -> bool:
        """
        Check if the file exists based on its relative path.

        Returns
        -------
        bool
            True if file exists otherwise False
        """
        return os.path.exists(self.file_name)

    def read_file(self) -> list[str]:
        """
        Read all the content of the current file. After reading strip all the lines and then upper the whole content.

        Returns
        -------
        list[str]
            A list of strings containing the lines of the file.
        """
        with open(file=self.file_name, mode='r') as file:
            return str.upper(''.join(file.readlines()).strip()).split('\n')

    def check_entries_integrity(self, records: list[str]) -> list[str]:
        """
        Checks the integrity of each record inside a list of strings based on a regex pattern. To be a valid record it
        must have at least one worked day alongside the name of the user.

        Example:

        - JOHN=00:00-10:00

        Parameters
        ----------
        records: list[str]
            A list of strings representing the entries in a file.

        Returns
        -------
        list[str]
            A curated list of records which meet regex pattern.
        """
        right_records = 0
        wrong_records = 0
        curated_records = list()
        for record in records:
            if len(self.regex.findall(record)) == 0:
                wrong_records += 1
                print(f'The record: {record} does not meet the required format, record removed...')
            else:
                curated_records.append(record)
                right_records += 1
        print(f'Number of records removed: {wrong_records}')
        print(f'Number of valid records: {right_records}')
        print(f'Total number of records: {(wrong_records+right_records)}')
        print('**'*20)
        return curated_records
