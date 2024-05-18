from flask import Flask
from config import Config
from model import db, bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from utils.celery_worker import celery_init_app
from celery.schedules import crontab
from utils import celery_task as tasks
from utils.librarian_setup import librarian_setup


app = Flask(__name__)
celery_app = celery_init_app(app)
app.config.from_object(Config)
db.init_app(app)

from routes import *
bcrypt.init_app(app)  #password hashing
jwt = JWTManager(app)  #JSON Web Tokens


CORS(app, resources={r"/*": {"origins": "*"}})
        
with app.app_context():
    db.create_all()

    # Create Librarian as Admin if not exists
    librarian_setup()   
    

#✌️❤️📚
# Run monthly activity report every minute  
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Reminding users to login
    sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.daily_reminders.s())

    # Update access logs
    sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.update_access_logs.s())

    # Monthly activity report
    sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.monthly_activity_report.s())
    

if __name__ == '__main__':

    app.run(debug=True)    