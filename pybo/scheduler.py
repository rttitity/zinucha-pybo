import requests
from datetime import datetime
from flask_apscheduler import APScheduler
from pybo import db
from pybo.models import TrainPosition

# 🚇 서울시 API 키
API_KEY = '69775968786a696e3236656859596b'

# ✅ 실제 API에 맞는 호선 ID 값
DEFAULT_LINES = ['1호선', '2호선']  # 1호선, 2호선

# 📅 스케줄러 객체 (app.py에서 init_app으로 초기화됨)
scheduler = APScheduler()

# 🔄 열차 위치를 주기적으로 수집하여 DB에 저장
def fetch_and_store_positions(app):
    with app.app_context():
        for line_id in DEFAULT_LINES:
            try:
                url = f"http://swopenAPI.seoul.go.kr/api/subway/{API_KEY}/json/realtimePosition/0/100/{line_id}"
                res = requests.get(url)
                data = res.json()

                if 'realtimePositionList' not in data:
                    print(f"[{datetime.now()}] ⚠️ {line_id} 데이터 없음")
                    continue

                for item in data['realtimePositionList']:
                    pos = TrainPosition(
                        train_no=item['trainNo'],
                        subway_id=item['subwayId'],
                        statn_nm=item['statnNm'],
                        statn_id=item.get('statnId'),
                        statn_tnm=item.get('statnTnm'),
                        recptn_dt=datetime.strptime(item['recptnDt'], '%Y-%m-%d %H:%M:%S'),
                        train_sttus=int(item.get('trainSttus', -1)),
                        updn_line=int(item.get('updnLine', -1)),
                        direct_at=int(item.get('directAt', 0)),
                        lstcar_at=int(item.get('lstcarAt', 0)),
                    )
                    db.session.add(pos)

                db.session.commit()
                print(f"[{datetime.now()}] ✅ {line_id} 열차 위치 저장 완료")
            except Exception as e:
                print(f"[{datetime.now()}] ❌ {line_id} 저장 실패: {e}")
