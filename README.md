# 신입사원 개인 프로젝트

- 게시판 제작 참고 사이트 https://wikidocs.net/book/4542

## config.py 구성

DB 연동시 config.py 구성 필요

- MySQL 연동시
```commandline
import os
DEBUG = True

# ✅ MySQL 연결
DB_USER = os.getenv("DB_USER", "MySQL 사용자명")
DB_PASSWORD = os.getenv("DB_PASSWORD", "MySQL 비밀번호")
DB_HOST = os.getenv("DB_HOST", "MySQL 도메인")
DB_PORT = os.getenv("DB_PORT", "포트번호")
DB_NAME = os.getenv("DB_NAME", "사용 데이터베이스 명")

# ✅ MySQL 연결 URI 설정
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

## 연관 라이브러리 설치 및 확인

- 설치된 패키지 목록 확인
```commandline
pip list
```
- 현재 설치된 패키지 `requirements.txt` 로 저장
```commandline
pip freeze > requirements.txt
```
- 연관 패키지 및 라이브러리 설치
```commandline
pip install -r requirements.txt
```

### 패키지 관련 특이사항

- `flaks-Markdown` 패키지 수동 설치
```commandline
git clone https://github.com/vanzhiganov/flask-markdown.git
cd flask-markdown
```

- setup.py 파일 열어서 다음 내용 수정
```commandline
version='dev' → version='0.1.0'
```

- pip install로 설치
```commandline
pip install .
```
