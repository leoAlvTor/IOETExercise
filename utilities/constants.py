
class Constants:
    # Constants for FileUtility class.

    # Regex for checking weekdays salary integrity
    SALARY_INTEGRITY_REGEX: str = r'[A-Z]+[0-9]+[0-9]+:[0-9]+-[0-9]+:[0-9]+'
    # Regex for checking full string integrity
    FULL_RECORD_REGEX: str = r'^[A-Z]+='+SALARY_INTEGRITY_REGEX

    # Constants for Payment class.
    WEEK_DAYS: list = ['MO', 'TU', 'WE', 'TH', 'FR']
    TIME_FORMAT: str = '%H:%M'

    WEEKEND_BONUS: int = 5
    FULL_WEEKEND_DAY_SALARY = 600
    FULL_WEEK_DAY_SALARY = 480

    WEEK_TIME_PAYMENT: dict = {
        '00:01-09:00': 25,
        '09:01-18:00': 15,
        '18:01-00:00': 20,
    }