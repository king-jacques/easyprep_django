from celery import shared_task
from django.core.mail import send_mail
from smtplib import SMTPException
from time import sleep

@shared_task
def do_something():
    sleep(1)
    #do something
    #call this function somewhere with do_something.delay(*args if any)