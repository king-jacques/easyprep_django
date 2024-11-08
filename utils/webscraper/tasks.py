from celery import Celery
from time import sleep
app = Celery('tasks', broker='amqp://localhost', backend='db+sqlite:///db2.sqlite3')

@app.task
def reverse(text):
    sleep(5)
    return text[::-1]

#celery -A utils.webscraper.tasks worker --loglevel=info


#in app
#result = reverse.delay('Anthony')
#result.status 
# 'PENDING'
#result.status 
# #'SUCCESS'
#result.get()
#'ynohtnA'
#