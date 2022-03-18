import os.path
from datetime import datetime as dt
import re


class Payment:
    user_input: str
    user_name: str

    WEEK_DAYS: list = ['MO', 'TU', 'WE', 'TH', 'FR']
    TIME_FORMAT: str = '%H:%M'

    week_time_hours: dict = {
        '00:01-09:00': (),
        '09:01-18:00': (),
        '18:01-00:00': ()
    }

    week_time_payment: dict = {
        '00:01-09:00': 25,
        '09:01-18:00': 15,
        '18:01-00:00': 20,
    }

    WEEKEND_BONUS: int = 5

    def __init__(self, user_input):
        self.__init_week_time_hours_dict()
        self.regular_expression = re.compile('[A-Z]+[0-9]+[0-9]+:[0-9]+-[0-9]+:[0-9]+')
        self.user_input = user_input

    def __init_week_time_hours_dict(self) -> None:
        for key in self.week_time_hours.keys():
            split_hours = key.split('-')
            self.week_time_hours[key] = (dt.strptime(split_hours[0], self.TIME_FORMAT).hour,
                                         dt.strptime(split_hours[1], self.TIME_FORMAT).hour)

    def get_worked_days(self) -> list:
        split_input = self.user_input.split('=')
        self.user_name = split_input[0]
        worked_days: list = self.regular_expression.findall(split_input[1])
        return worked_days

    def split_time(self, hours: list) -> tuple:
        return dt.strptime(hours[0], '%H:%M').hour, dt.strptime(hours[1], '%H:%M').hour

    def calculate_hour_price(self, day: str, start_time, end_time) -> float:
        price = 0
        for key, time_tuple in self.week_time_hours.items():
            value = list(time_tuple)
            value[1] = 24 if value[1] == 0 else value[1]
            end_time = 24 if end_time == 0 else end_time
            if start_time >= value[0] and end_time <= value[1]:
                week_payment = self.week_time_payment.get(key) if day in self.WEEK_DAYS else self.week_time_payment.get(
                    key) + self.WEEKEND_BONUS
                return abs(end_time - start_time) * week_payment
            elif start_time >= value[0] and end_time > value[1]:
                price = abs(value[1] - start_time) * self.week_time_payment.get(key)
                continue
            elif start_time < value[0] and end_time <= value[1]:
                week_payment = self.week_time_payment.get(key) if day in self.WEEK_DAYS else self.week_time_payment.get(
                    key) + self.WEEKEND_BONUS
                return abs(end_time - value[0]) * week_payment + price

    def __get_next_day(self, current_day: str):
        if current_day == 'FR':
            return 'SA'
        elif current_day == 'SU':
            return 'MO'
        else:
            return self.WEEK_DAYS[self.WEEK_DAYS.index(current_day)+1]

    def calculate_salary(self, worked_days: list) -> float:
        salary: float = 0
        for element in worked_days:
            day, hours = element[0:2], element[2:].split('-')
            start_hour, end_hour = self.split_time(hours)
            if start_hour > end_hour:
                salary += self.calculate_hour_price(day, start_hour, 0)
                salary += self.calculate_hour_price(self.__get_next_day(day), 0, end_hour)
                continue
            salary += self.calculate_hour_price(day, start_hour, end_hour)
        return salary

    def get_output(self, salary: float) -> str:
        return f'The amount to pay {self.user_name} is: {salary} USD'

    @staticmethod
    def open_file(file_name: str = 'ACME payment.txt') -> list:
        if not os.path.exists(file_name):
            raise 'error: File not found!'
        with open(file_name, 'r') as file:
            file_text: list = ''.join(file.readlines()).split('\n')
        return file_text
