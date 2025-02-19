
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import utc



jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

# Scheduler setup
scheduler = BackgroundScheduler(daemon=True)  # ✅ Ensures it runs in the background
scheduler.configure(timezone=utc)
        
scheduler.start()