import sys
import payment

if __name__ == '__main__':
    if len(sys.argv) < 1:
        raise 'Error, no input received'
    else:
        paymentList = payment.Payment.open_file(sys.argv[1])

        for paymentString in paymentList:
            paymentObject = payment.Payment(paymentString)
            worked_days = paymentObject.get_worked_days()
            if len(worked_days) > 0:
                salary = paymentObject.calculate_salary(worked_days)
                output = paymentObject.get_output(salary)
                print(output)
            else:
                raise Exception('Payment string does not match pattern XX00:00-00:00 where XX represents the first '
                                'two letters of week day.')
