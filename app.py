from flask import Flask
from flaskext.markdown import Markdown
from pybo import db, migrate, scheduler  # ✅ 확장 객체 import
from pybo.scheduler import fetch_and_store_positions    # 스케줄 라이브러리
from flask_session import Session

from datetime import datetime
import socket
import config
import redis


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM 초기화
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # PostgreSQL 사용시 search_path 강제 세팅
    from sqlalchemy import event

    # 앱 컨텍스트 안에서 엔진을 가져와 event 등록
    schema = app.config.get("DB_SCHEMA", "myapp")

    def _set_search_path(dbapi_conn, connection_record):
        cur = dbapi_conn.cursor()
        cur.execute(f'SET search_path TO "{schema}"')
        cur.close()

    with app.app_context():
        engine = db.get_engine(app)      # <- 컨텍스트 안에서 엔진 획득
        event.listen(engine, "connect", _set_search_path)

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

    # # Redis 연결 구성
    # app.config['SESSION_TYPE'] = config.SESSION_TYPE
    # app.config['SESSION_PERMANENT'] = config.SESSION_PERMANENT
    # app.config['SESSION_USE_SIGNER'] = config.SESSION_USE_SIGNER
    # app.config['SESSION_KEY_PREFIX'] = config.SESSION_KEY_PREFIX
    #
    # app.config['SESSION_REDIS'] = redis.StrictRedis(
    #     host=app.config['SESSION_REDIS_HOST'],
    #     port=app.config['SESSION_REDIS_PORT'],
    #     # password=app.config['SESSION_REDIS_PASSWORD'],
    #     decode_responses=False
    # )

    Session(app)

    # ✅ APScheduler 초기화 및 작업 등록
    # scheduler.init_app(app)
    # scheduler.start()
    # scheduler.add_job(
    #     id='FetchTrainPositions',
    #     func=lambda: fetch_and_store_positions(app),
    #     trigger='interval',
    #     seconds=30
    # )

    # Flask 세션 사용시 쿠키에 세션id 저장 - 쿠키 헤더 초과 오류 발생
    @app.before_request
    def set_session_id():
        from flask import request, session
        session['_id'] = request.cookies.get('session', 'N/A')


    @app.context_processor
    def inject_server_info():
        from flask import request
        return {
            'hostname': socket.gethostname(),
            'server_ip': socket.gethostbyname(socket.gethostname()),
            'session_id': request.cookies.get('session', 'N/A'),
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }


    return app

