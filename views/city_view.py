# city_view module in views/city_view.py

from flask import jsonify, Blueprint
from models.city import City
from extensions import redis_client
import json

city_view = Blueprint('city_view', __name__)


@city_view.route('/api/cities', methods=['GET'])
def get_cities():
    cache_key = "cities"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return jsonify(json.loads(cached_data))

    cities = City.query.all()
    result = [city.name for city in cities]
    redis_client.setex(cache_key, 3600, json.dumps(result))
    return jsonify(result)