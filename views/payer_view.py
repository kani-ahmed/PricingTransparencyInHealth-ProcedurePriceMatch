# payer_view module in views/payer_view.py

from flask import jsonify, Blueprint, request
from models.payer import Payer
from models.zipcode import ZipCode
from models.hospital import Hospital
from extensions import redis_client
import json

payer_view = Blueprint('payer_view', __name__)


@payer_view.route('/api/payers', methods=['GET'])
def get_payers():
    zipcode = request.args.get('zipcode')
    hospital_name = request.args.get('hospital')
    cache_key = f"payers:{zipcode}:{hospital_name}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data))

    query = Payer.query

    if hospital_name:
        hospital_obj = Hospital.query.filter_by(name=hospital_name).first()
        if hospital_obj:
            zipcode_obj = ZipCode.query.filter_by(id=hospital_obj.zipcode_id).first()
        else:
            return jsonify([])
    elif zipcode:
        zipcode_obj = ZipCode.query.filter_by(code=zipcode).first()
    else:
        result = [payer.name for payer in Payer.query.all()]
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result)

    if zipcode_obj:
        payers = query.join(Payer.zipcodes).filter_by(id=zipcode_obj.id).all()
    else:
        payers = []

    result = [payer.name for payer in payers]
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return jsonify(result)
