from test_cases.payment_test_cases import Payment
from utilities.file_utility import FileUtility


def get_welcome_str() -> str:
    return """
    ** Welcome **
    Please select one of the next options:
    1. Read a file of records and get the output.
    2. Exit
    """


def choose_option():
    option = int(input('Enter an option: ').strip())
    if option == 1:
        return execute_code()
    else:
        finish_execution()


def execute_code() -> bool:
    file = input('Enter the file name: ')
    file_utility_object = FileUtility(file_name=file)
    if not file_utility_object.check_file_exists():
        print(f'The file {file} does not exists!')
        return False
    else:
        payment_records = file_utility_object.read_file()
        payment_records = file_utility_object.check_entries_integrity(payment_records)
        for payment_record in payment_records:
            payment_object = Payment(payment_record)
            worked_days = payment_object.get_worked_days()
            salary = payment_object.calculate_salary(worked_days)
            output = payment_object.get_output(salary)
            print(output)
        return True


def finish_execution():
    print('Bye!')
    exit(0)

