# comprehend_medical_service.py
from flask import request, jsonify, Blueprint
import boto3, json, os
from sqlalchemy.orm import joinedload
from extensions import redis_client
from models.icd_cpt_mapping import IcdCptMapping
from models.hospital_charge import HospitalCharge
from models import CptTranslation

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

comprehend_medical_blueprint = Blueprint('comprehend_medical', __name__)
session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION)
comprehend = session.client('comprehendmedical')

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


@comprehend_medical_blueprint.route('/api/comprehend-medical', methods=['POST'])
def comprehend_medical():
    data = request.get_json()
    user_chatbox_data = json.loads(data['user_chatbox_data'])
    city = user_chatbox_data.get('city')
    zipcode = user_chatbox_data.get('zipcode')
    page = int(user_chatbox_data.get('page', 1))
    per_page = int(user_chatbox_data.get('per_page', 100))
    description = user_chatbox_data['description']
    filters = user_chatbox_data.get('filters', [])

    # Base cache key for all results based on input parameters
    base_cache_key = f"comprehend:{city}:{zipcode}:{description}:{json.dumps(filters)}"

    # Try fetching the full result set from cache
    full_results_cache = redis_client.get(base_cache_key)
    if full_results_cache:
        full_results = json.loads(full_results_cache)
    else:
        icd_codes = fetch_or_compute_icd_codes(description, base_cache_key)
        cpt_codes = fetch_cpt_codes(icd_codes)
        query = build_query(city, zipcode, cpt_codes, filters)
        charges = query.all()
        full_results = [build_result(charge) for charge in charges]
        # Cache the comprehensive results
        redis_client.setex(base_cache_key, 3600, json.dumps(full_results))

    # Pagination logic
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = full_results[start:end]

    return jsonify({
        'results': paginated_results,
        'page': page,
        'total_pages': (len(full_results) + per_page - 1) // per_page,
        'total_results': len(full_results)
    })


def fetch_or_compute_icd_codes(description, comprehend_cache_key):
    icd_cache = redis_client.get(comprehend_cache_key)
    if not icd_cache:
        input_text = f"Description: {description}"
        response = comprehend.infer_icd10_cm(Text=input_text)
        icd_codes = list(
            set(concept['Code'] for entity in response['Entities'] for concept in entity['ICD10CMConcepts']))
        redis_client.setex(comprehend_cache_key, 8600, json.dumps(icd_codes))
    else:
        icd_codes = json.loads(icd_cache)
    return icd_codes


def fetch_cpt_codes(icd_codes):
    cpt_codes = [mapping.CPT_Code for mapping in
                 IcdCptMapping.query.filter(IcdCptMapping.ICD_Code.in_(icd_codes)).distinct()]
    return list(set(cpt_codes))


def build_query(city, zipcode, cpt_codes, filters):
    query = HospitalCharge.query.options(joinedload(HospitalCharge.cpt_translation)).filter(
        HospitalCharge.Associated_Codes.in_(cpt_codes))
    if city:
        query = query.filter_by(City=city)
    if zipcode:
        query = query.filter_by(ZipCode=zipcode)
    for filter_dict in filters:
        filter_type = filter_dict['filterType']
        filter_query = filter_dict['filterQuery']
        query = query.filter(getattr(HospitalCharge, COLUMN_NAME_MAPPING[filter_type]).like(f"%{filter_query}%"))
    return query


def build_result(charge):
    return {
        "Hospital": charge.Hospital,
        "CPT Code": charge.Associated_Codes,
        "Description": charge.cpt_translation.Description if charge.cpt_translation else 'N/A',
        "Cash Discount": str(charge.Cash_Discount) if charge.Cash_Discount else 'N/A',
        "Max Allowed": str(charge.Deidentified_Max_Allowed) if charge.Deidentified_Max_Allowed else 'N/A',
        "Min Allowed": str(charge.Deidentified_Min_Allowed) if charge.Deidentified_Min_Allowed else 'N/A',
        "Payer": charge.payer if charge.payer else 'N/A',
        "IOB Selection": charge.iobSelection if charge.iobSelection else 'N/A',
    }
