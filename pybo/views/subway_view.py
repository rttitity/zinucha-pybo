from flask import Blueprint, render_template, jsonify, request, Response
import requests
import json
from config import SUBWAY_POSITION_API_KEY

bp = Blueprint('subway', __name__, url_prefix='/subway')

@bp.route('/')
def subway_page():
    return render_template('subway/subway.html')

@bp.route('/position')
def get_subway_position():
    # ✅ JS에서 보내는 line_id 값 받기 (기본값은 1002 → 2호선)
    line_id = request.args.get('line_id', '2호선')

    url = f"http://swopenAPI.seoul.go.kr/api/subway/{SUBWAY_POSITION_API_KEY}/json/realtimePosition/0/50/{line_id}"

    try:
        response = requests.get(url)
        data = response.json()

        print("✅ API 응답 구조:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return Response(json.dumps(data, ensure_ascii=False), content_type='application/json; charset=utf-8')
    except Exception as e:
        return jsonify({'error': str(e)})
