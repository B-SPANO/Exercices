from .celery import app
# from celery.schedules import crontab
from forum.mail import sendmail

@app.task
def sendmail_task():
    sendmail()


if __name__ == '__main__':
    app.worker_main()