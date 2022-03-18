import sys
import payment

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise 'Error, no input received'
    else:
        payment = payment.Payment(sys.argv[1])
        worked_days = payment.get_worked_days()
        payment.calculate_salary(worked_days)
