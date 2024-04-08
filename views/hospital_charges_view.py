import json

from flask import jsonify, request, Blueprint

from extensions import redis_client
from models import CptTranslation
from models.hospital_charge import HospitalCharge
from sqlalchemy.orm import joinedload

hospital_charges_view = Blueprint('hospital_charges_view', __name__)

COLUMN_NAME_MAPPING = {
    "Hospital": "Hospital",
    "CPT Code": "Associated_Codes",
    # "Description": "cpt_translation.Description",
    "Cash Discount": "Cash_Discount",
    "Min Allowed": "Deidentified_Min_Allowed",
    "Max Allowed": "Deidentified_Max_Allowed",
    "Payer": "payer",
    "IOB Selection": "iobSelection",
}


@hospital_charges_view.route('/api/hospital_charges', methods=['POST'])
def get_hospital_charges():
    data = request.get_json()
    city = data.get('city')
    zipcode = data.get('zipcode')
    page = data.get('page', 1)
    per_page = data.get('per_page', 100)

    # Dynamic filter parameters
    filters = data.get('filters', [])  # Expect 'filters' to be a list of dictionaries

    # Construct a cache key from the request parameters
    cache_key = f"hospital_charges:{city}:{zipcode}:{page}:{per_page}:{str(filters)}"

    # Attempt to fetch cached data
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # If cache hit, return the cached data
        return jsonify(json.loads(cached_data))

    # Start with a base query
    query = HospitalCharge.query.options(joinedload(HospitalCharge.cpt_translation))

    # Apply city and zipcode filters
    if city:
        query = query.filter_by(City=city)
    if zipcode:
        query = query.filter_by(ZipCode=zipcode)

        # Process each filter in the filters list
        # Process each filter in the filters list
        for filter_dict in filters:
            filter_type = filter_dict.get('filterType')
            filter_query = filter_dict.get('filterQuery')

            if filter_type and filter_query:
                if filter_type == "Description":
                    # Apply filter on CptTranslation.Description
                    # Ensure to join with CptTranslation if filtering by Description
                    query = query.join(HospitalCharge.cpt_translation).filter(
                        CptTranslation.Description.like(f"%{filter_query}%"))
                else:
                    # Apply filter directly on HospitalCharge attributes
                    # Use COLUMN_NAME_MAPPING to get the correct attribute name
                    filter_key = COLUMN_NAME_MAPPING.get(filter_type)
                    if filter_key:
                        query = query.filter(getattr(HospitalCharge, filter_key).like(f"%{filter_query}%"))

        charges = query.paginate(page=page, per_page=per_page)

    results = [build_result(charge) for charge in charges.items]

    # After fetching data from the database and preparing the results...
    # Cache the response data
    redis_client.setex(cache_key, 3600, json.dumps({
        'results': results,
        'page': charges.page,
        'total_pages': charges.pages,
        'total_results': charges.total
    }))  # 3600 seconds = 1 hour cache expiration

    return jsonify({
        'results': results,
        'page': charges.page,
        'total_pages': charges.pages,
        'total_results': charges.total
    })


def build_result(charge):
    return {
        "CPT Code": charge.Associated_Codes,
        "Description": charge.cpt_translation.Description if charge.cpt_translation else 'N/A',
        "Cash_Discount": str(charge.Cash_Discount),
        "Deidentified_Max_Allowed": charge.Deidentified_Max_Allowed,
        "Deidentified_Min_Allowed": str(charge.Deidentified_Min_Allowed),
        "payer": charge.payer,
        "iobSelection": charge.iobSelection,
        "Hospital": charge.Hospital
    }