# scheduler_worker.py
from pybo import scheduler
from app import create_app
from pybo.scheduler import fetch_and_store_positions

app = create_app()
with app.app_context():
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(
        id='FetchTrainPositions',
        func=lambda: fetch_and_store_positions(app),
        trigger='interval',
        seconds=30
    )
    print("✅ Scheduler is running...")
    scheduler._event.wait()  # 종료 방지
