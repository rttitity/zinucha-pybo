from flask import Flask
from flaskext.markdown import Markdown
from pybo import db, migrate, scheduler  # ✅ 확장 객체 import
from pybo.scheduler import fetch_and_store_positions
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM 초기화
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # 블루프린트 등록
    from pybo.views import main_views, question_views, answer_views, auth_views, subway_view
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(subway_view.bp)

    # 필터 등록
    from pybo.filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # Markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # ✅ APScheduler 초기화 및 작업 등록
    # scheduler.init_app(app)
    # scheduler.start()
    # scheduler.add_job(
    #     id='FetchTrainPositions',
    #     func=lambda: fetch_and_store_positions(app),
    #     trigger='interval',
    #     seconds=30
    # )

    return app
