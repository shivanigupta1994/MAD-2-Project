from celery import shared_task, Celery
from utils.mail_hog import send_email
from datetime import datetime
from utils.email_templates import create_html_reminder, create_html_report, google_chat_webhook
from model import User, db, AccessLog


@shared_task(ignore_result=True)
def daily_reminders():
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    Users = User.query.filter_by(user_type='user').all()
    
    for user in Users:
        if user.last_login != current_date:
            html_reminder = create_html_reminder(user)
            send_email(user.email, 'Reminder', html_reminder)
            google_chat_webhook(user.username)
    


@shared_task(ignore_result=True)
def monthly_activity_report():

    Users = User.query.filter_by(user_type='user').all()
    AccessLogs = AccessLog.query.all()

    for user in Users:
        books_borrowed = []
        for log in AccessLogs:
            if log.user_id == user.id:
                books_borrowed.append(log)
        
        html_report = create_html_report(username=user.username, access_logs=books_borrowed)
        send_email(user.email, 'Monthly Activity Report', html_report)
        print('Monthly Activity Report sent to ' + user.username)



@shared_task(ignore_result=True)
def update_access_logs():
    issued_logs = AccessLog.query.filter_by(status='Issued').all()
    count = 0
    for log in issued_logs:
        if datetime.now() > log.due_date:
            count += 1
            print('Book overdue of '+ log.username +" with book  ==>   "+ log.book_name)
            print('Updating access log for User '+ log.username)
            log.status = 'Revoked'
            db.session.commit()    
    print('Access logs updated '+ str(datetime.now()))  
    print('Total books overdue: '+ str(count))      