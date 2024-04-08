# Adjusted hospital_view module in views/hospital_view.py

from flask import jsonify, Blueprint, request
from models.hospital import Hospital
from models.zipcode import ZipCode
from extensions import redis_client
import json

hospital_view = Blueprint('hospital_view', __name__)


@hospital_view.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    zipcode = request.args.get('zipcode')
    cache_key = f"hospitals:{zipcode}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data))

    if zipcode:
        zipcode_obj = ZipCode.query.filter_by(code=zipcode).first()
        if zipcode_obj:
            hospitals = Hospital.query.filter_by(zipcode_id=zipcode_obj.id).all()
        else:
            hospitals = []
    else:
        hospitals = Hospital.query.all()

    result = [hospital.name for hospital in hospitals]
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return jsonify(result)
