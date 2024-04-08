# zipcodes view in views/zipcode_view.py

from flask import jsonify, Blueprint, request
from models.zipcode import ZipCode
from models.city import City
from extensions import redis_client
import json

zipcode_view = Blueprint('zipcode_view', __name__)


@zipcode_view.route('/api/zipcodes', methods=['GET'])
def get_zipcodes():
    city = request.args.get('city')
    cache_key = f"zipcodes:{city}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data))

    if city:
        city_obj = City.query.filter_by(name=city).first()
        if city_obj:
            zipcodes = ZipCode.query.filter_by(city_id=city_obj.id).all()
        else:
            zipcodes = []
    else:
        zipcodes = ZipCode.query.all()

    result = [zipcode.code for zipcode in zipcodes]
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return jsonify(result)
