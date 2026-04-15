from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
def post_job(text, platforms):
    from poster import post_to_platforms
    post_to_platforms(text, platforms)
    print(f"[POST] {datetime.now()} | Platforms: {platforms} | Text: {text}")


def schedule_post(text, platforms, dt):
    scheduler.add_job(post_job, 'date', run_date=dt, args=[text, platforms])
    # Save to database
    from database import save_scheduled_post
    save_scheduled_post(text, platforms, dt)
