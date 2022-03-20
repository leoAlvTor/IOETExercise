import os.path
from datetime import datetime as dt
import re


class Payment:
    """
    Class for calculating the payment of an employee.
    """
    user_input: str
    user_name: str

    WEEK_DAYS: list = ['MO', 'TU', 'WE', 'TH', 'FR']
    TIME_FORMAT: str = '%H:%M'

    week_time_hours: dict = {
        '00:01-09:00': [],
        '09:01-18:00': [],
        '18:01-00:00': []
    }

    week_time_payment: dict = {
        '00:01-09:00': 25,
        '09:01-18:00': 15,
        '18:01-00:00': 20,
    }

    WEEKEND_BONUS: int = 5
    FULL_WEEKEND_DAY_SALARY = 600
    FULL_WEEK_DAY_SALARY = 480

    def __init__(self, user_input: str):
        """
        Initialize the main variables for the class.

        Parameters
        ----------
        user_input: str
            The user input as string. It contains the username and its worked hour/s.
        """
        self.__init_week_time_hours_dict()
        self.regular_expression = re.compile('[A-Z]+[0-9]+[0-9]+:[0-9]+-[0-9]+:[0-9]+')
        self.user_input = user_input
        self.user_name = user_input.split('=')[0]

    def __init_week_time_hours_dict(self):
        """
        Extract the hour from the keys in week_time_hours dictionary and updates their keys with a pair of initial hour
        and the ending hour.
        """
        for key in self.week_time_hours.keys():
            split_hours = key.split('-')
            self.week_time_hours[key] = [dt.strptime(split_hours[0], self.TIME_FORMAT).hour,
                                         dt.strptime(split_hours[1], self.TIME_FORMAT).hour]

    def get_worked_days(self) -> list:
        """
        Extracts all worked days based on the next statement using regex and stores it in a list:

        day + start_hour + '-' + end_hour

        * start_hour and end_hour are in 24-hour format

        Returns
        -------
        list
            A list of strings containing worked days.
        """
        return self.regular_expression.findall(self.user_input.split('=')[1])

    def get_hours_from_string(self, hours: list) -> tuple:
        """
        Parse each string in a list to time instances. Then extract their hour from each instance.

        Parameters
        ----------
        hours: list
            A list containing two strings, the start_hour and the end_hour.
            For example ['12:00', '18:00'] becomes 12 and 18.

        Return
        -------
        tuple
            A tuple representing start_hour and end_hour.

        Raises
        ------
        Exception
            If the string doesn't meet the format HH:MM or if the hour is higher than 24.
            For example ['25:00']
        """
        try:
            start = dt.strptime(hours[0], '%H:%M').hour
            end = dt.strptime(hours[1], '%H:%M').hour
        except Exception:
            raise Exception(f'Error while parsing the string: {hours} for user {self.user_name}')
        return start, end

    def check_days_validity(self, day: str) -> bool:
        """
        Check if working day format is valid.

        Parameters
        ----------
        day: str
            A string representing the current work day

        Returns
        -------
        bool
            True if day is a valid weekday otherwise False

        """
        return day in self.WEEK_DAYS + ['SA', 'SU']

    def check_hours_validity(self, start_end_pair: list, end_time: int) -> tuple:
        """
        Check hours' validity for example if end_hour is 0 then it becomes 24 (the end of the day).

        Parameters
        ----------
        start_end_pair: list
            A list containing start_hour and end_hour of the current day.

        end_time: int
            The end time of the current worked day.

        Returns
        -------
        tuple
            A tuple containing a list with its formatted hours and an int with its formatted hour.
        """
        start_end_pair[1] = 24 if start_end_pair[1] == 0 else start_end_pair[1]
        end_time = 24 if end_time == 0 else end_time
        return start_end_pair, end_time

    def calculate_salary_per_hours(self, day: str, start_time: int, end_time: int) -> float:
        """
        Calculates the price per worked hours.

        Consideration to calculate the salary:

        - If the current day is a weekend day then hour payment range value increases its value by 5 dollars.

        Parameters
        ----------
        day: str
            The current worked day.

        start_time: int
            The hour in which the day began.

        end_time: int
            The hour in which the day ended.

        Returns
        -------
        float
            A float number in representation of the salary of the worked hours.
        """
        price = 0
        for key, value in self.week_time_hours.items():
            value, end_time = self.check_hours_validity(value, end_time)
            week_payment = self.week_time_payment.get(key) if day in self.WEEK_DAYS else self.week_time_payment.get(
                key) + self.WEEKEND_BONUS
            if start_time >= value[0] and end_time <= value[1]:
                return (end_time - start_time) * week_payment
            elif start_time >= value[0] and end_time >= value[1]:
                price = (value[1] - start_time) * week_payment
            elif start_time < value[0] and end_time <= value[1]:
                return (end_time - value[0]) * week_payment + price
            elif start_time <= value[0] and end_time >= value[1]:
                price += (value[1]-value[0]) * week_payment

    def get_next_day(self, current_day: str) -> str:
        """
        Get the next day of the week based on the current day.

        Parameters
        ----------
        current_day: str
            The current working day.

        Returns
        -------
        str
            A string in a representation of the next weekday.
        """
        if current_day == 'FR':
            return 'SA'
        elif current_day == 'SA':
            return 'SU'
        elif current_day == 'SU':
            return 'MO'
        else:
            return self.WEEK_DAYS[self.WEEK_DAYS.index(current_day) + 1]

    def calculate_whole_day(self, is_weekend: bool, day: str, start_hour: int, end_hour: int) -> float:
        """
        Calculates the whole day salary when start_hour and end_hour matches or when start_hour is greater than
        end_hour.\n
        For example:

        - SU00:00-00:00. (Whole day calculation for a weekend day)
        - TU10:00-07:00. (Whole day calculation from 10am to 00am and from 00am to 07am)

        Consideration for calculating the whole day salary:\n
        - If the current day is weekend and the start_hour and end_hour are 0 (zero) then the salary become $600
        - If the start_hour and end_hour are not 0 (zero) then salary calculation is divided to the end of the start
        hour and from hour zero to the ending hour.

        Parameters
        ----------
        is_weekend: bool
            Checks if the current day is a weekend day.

        day: str
            The current weekday.

        start_hour: int
            The hour in which the day began.

        end_hour: int
            The hour in which the day ended.

        Returns
        -------
        float
            A float containing the salary.
        """
        if is_weekend and end_hour == 0:
            return self.FULL_WEEKEND_DAY_SALARY
        else:
            salary = self.calculate_salary_per_hours(day, start_hour, 24) \
                     + self.calculate_salary_per_hours(self.get_next_day(day), 0, end_hour)
            return salary

    def calculate_salary(self, worked_days: list) -> float:
        """
        Determines how the salary will be calculated considering special cases.

        Considerations for salary calculation:

        - If the start_hour is greater than end_hour then the salary is calculated in two parts using the method
        calculate_whole_day.

        - If the start_hour and end_hour are equal and the current day is between Monday to Thursday or the start_hour
        and the end_hour are zero and the current day is Friday then the salary becomes FULL_WEEK_DAY_SALARY.

        - If the start_hour and end_hour are equal, and for rejection the current day is a Weekend day then the
        method calculate_whole_day is invoked.

        - If none of the above conditions are meet then the method calculate_salary_per_hours is invoked.


        Parameters
        ----------
        worked_days: list
            A list of day and hours worked pairs as strings.

        Returns
        -------
        float
            The cumulative salary of a list of worked days.

        """
        salary = 0
        for element in worked_days:
            day, hours = element[0:2], element[2:].split('-')
            start_hour, end_hour = self.get_hours_from_string(hours)
            if start_hour > end_hour:
                salary += self.calculate_whole_day(is_weekend=False, day=day, start_hour=start_hour, end_hour=end_hour)
            elif (start_hour == end_hour and day not in ['FR', 'SA', 'SU']) or (start_hour == end_hour == 0 and day == 'FR'):
                salary += self.FULL_WEEK_DAY_SALARY
            elif start_hour == end_hour:
                salary += self.calculate_whole_day(is_weekend=True, day=day, start_hour=start_hour, end_hour=end_hour)
            else:
                salary += self.calculate_salary_per_hours(day, start_hour, end_hour)
        return salary

    def get_output(self, salary: float) -> str:
        """
        Generates a string containing the username and its salary.

        Parameters
        ----------
        salary: float
            The cumulative salary of the current user.

        Returns
        -------
        str
            The generated string containing the username and salary.
        """
        return f'The amount to pay {self.user_name} is: {salary} USD'

    @staticmethod
    def open_file(file_name: str = 'ACME payment.txt') -> list:
        """
        Opens a file and reads all its lines.

        Parameters
        ----------
        file_name: str
            The file name, by default it will be 'ACME payment.txt'

        Returns
        -------
        list
            A list of strings read from the file
        """
        if not os.path.exists(file_name):
            raise Exception(f'File not found!, file name: {file_name}')
        with open(file_name, 'r') as file:
            file_text = str.upper(''.join(file.readlines())).split('\n')
            return file_text
