from datetime import datetime as dt


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

    weekend_bonus: int = 5

    def __init__(self, user_input):
        self.__init_week_time_hours_dict()
        self.user_input = user_input

    def __init_week_time_hours_dict(self) -> None:
        for key in self.week_time_hours.keys():
            split_hours = key.split('-')
            self.week_time_hours[key] = (dt.strptime(split_hours[0], self.TIME_FORMAT).hour,
                                         dt.strptime(split_hours[1], self.TIME_FORMAT).hour)

    def get_worked_days(self) -> list:
        split_input = self.user_input.split('=')
        self.user_name = split_input[0]
        worked_days: list = split_input[1].split(',')
        return worked_days

    def split_time(self, hours: list) -> tuple:
        return dt.strptime(hours[0], '%H:%M').hour, dt.strptime(hours[1], '%H:%M').hour

    def calculate_hour_price(self, day: str, hours: list) -> float:
        start_time, end_time = self.split_time(hours)
        price = 0
        for key, time_tuple in self.week_time_hours.items():
            value = list(time_tuple)
            value[1] = 24 if value[1] == 0 else value[1]
            if start_time >= value[0] and end_time <= value[1]:
                week_payment = self.week_time_payment.get(key) if day in self.WEEK_DAYS else self.week_time_payment.get(
                    key) + 5
                return abs(end_time - start_time) * week_payment
            elif start_time >= value[0] and end_time > value[1]:
                price = abs(value[1] - start_time) * self.week_time_payment.get(key)
                continue
            elif start_time < value[0] and end_time <= value[1]:
                week_payment = self.week_time_payment.get(key) if day in self.WEEK_DAYS else self.week_time_payment.get(
                    key) + 5
                return abs(end_time - value[0]) * week_payment + price

    def calculate_salary(self, worked_days: list) -> float:
        salary = 0
        for element in worked_days:
            day: str = element[0:2]
            hours: list = element[2:].split('-')
            salary += self.calculate_hour_price(day, hours)
        return salary
