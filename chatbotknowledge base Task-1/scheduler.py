
import os, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from ingest import ingest_once
from dotenv import load_dotenv

load_dotenv()
POLL_MINUTES = int(os.getenv('POLL_INTERVAL_MINUTES', '60'))

scheduler = BlockingScheduler()

def job():
    print('Running ingestion job...')
    try:
        ingest_once()
    except Exception as e:
        print('Ingestion job error:', e)

if __name__ == '__main__':
    # Run once immediately
    job()
    scheduler.add_job(job, IntervalTrigger(minutes=POLL_MINUTES))
    print('Scheduler started. Poll interval (minutes):', POLL_MINUTES)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('Scheduler stopped.')
