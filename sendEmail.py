import sendgrid
import sys
import os
from sendgrid.helpers.mail import *


def send_notification_email(email_sent_to, heart_rate, date_string):
    """

    :param email_sent_to:
    :param heart_rate:
    :param date_string:
    :return:
    """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("i.liangzisheng@gmail.com")
    to_email = Email(email_sent_to)
    subject = "Warning: the heart rate is abnormal!"
    ctt_str = "Your last measured heart rate is abnormal, ({} at date {}), " \
              "Take care!".format(heart_rate, date_string)
    ctt = Content("text/plain", ctt_str)
    notif_mail = Mail(from_email, subject, to_email, ctt)
    response = sg.client.mail.send.post(request_body=notif_mail.get())
    return response.status_code


def main():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("i.liangzisheng@gmail.com")
    to_email = Email("error.zero.always@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == "__main__":
    sys.exit(main())



