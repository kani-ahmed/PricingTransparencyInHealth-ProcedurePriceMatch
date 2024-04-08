# comprehend_medical_service.py
import json
from flask import request, jsonify, Blueprint
import boto3
from sqlalchemy.orm import joinedload
from extensions import redis_client  # Assuming you have this setup similar to your example
from models.icd_cpt_mapping import IcdCptMapping
from models.hospital_charge import HospitalCharge

comprehend_medical_blueprint = Blueprint('comprehend_medical', __name__)

# Assume AWS session setup is similar to before
session = boto3.Session(region_name='us-east-2')
comprehend = session.client('comprehendmedical')


@comprehend_medical_blueprint.route('/api/comprehend-medical', methods=['POST'])
def comprehend_medical():
    input_data = request.get_json()
    user_chatbox_data = json.loads(input_data['user_chatbox_data'])

    city = user_chatbox_data['city']
    zipcode = user_chatbox_data['zipcode']
    description = user_chatbox_data['description']

    input_text = f"Description: {description}"
    response = comprehend.infer_icd10_cm(Text=input_text)
    entities = response['Entities']

    # Extract ICD-10-CM codes
    icd_codes = [concept['Code'] for entity in entities for concept in entity['ICD10CMConcepts']]
    # remove duplicates
    icd_codes = list(set(icd_codes))

    print(f"Extracted ICD-10-CM codes: {icd_codes}")
    # Query IcdCptMappings to get CPT codes related to the extracted ICD-10-CM codes
    cpt_codes = IcdCptMapping.query.filter(IcdCptMapping.ICD_Code.in_(icd_codes)).distinct(IcdCptMapping.CPT_Code).all()
    cpt_codes_list = [mapping.CPT_Code for mapping in cpt_codes]
    # remove duplicates
    cpt_codes_list = list(set(cpt_codes_list))
    print(f"Related CPT codes: {cpt_codes_list}")
    # Use the CPT codes to filter HospitalCharges
    hospital_charges_query = HospitalCharge.query.options(joinedload(HospitalCharge.cpt_translation)).filter(
        HospitalCharge.Associated_Codes.in_(cpt_codes_list),
        HospitalCharge.City == city,
        HospitalCharge.ZipCode == zipcode
    )
    # Optional: paginate or limit the query results if necessary
    hospital_charges = hospital_charges_query.limit(100).all()
    print(f"Found {len(hospital_charges)} hospital charges matching the criteria")
    results = [build_result(charge) for charge in hospital_charges]
    print(f"Results of found hospitals: {results}")

    return jsonify(results)


def build_result(charge):
    return {
        "Description": charge.cpt_translation.Description if charge.cpt_translation else 'N/A',
        "Hospital": charge.Hospital,
        "Cash Discount": str(charge.Cash_Discount) if charge.Cash_Discount else 'N/A',
        "Max Allowed": charge.Deidentified_Max_Allowed if charge.Deidentified_Max_Allowed else 'N/A',
        "Min Allowed": str(charge.Deidentified_Min_Allowed) if charge.Deidentified_Min_Allowed else 'N/A',
        "Payer": charge.payer if charge.payer else 'N/A',
        "IOB Selection": charge.iobSelection if charge.iobSelection else 'N/A'
    }
