from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from sqlalchemy import MetaData

# Naming convention (for Alembic migrations)
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 전역 확장 객체 선언 (app.py에서 init_app으로 초기화됨)
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
scheduler = APScheduler()
