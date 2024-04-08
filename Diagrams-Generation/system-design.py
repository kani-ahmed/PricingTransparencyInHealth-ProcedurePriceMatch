from diagrams import Diagram, Cluster, Edge
from diagrams.generic.database import SQL
from diagrams.programming.framework import Vue, Fastapi
from diagrams.programming.framework import Flask
from diagrams.custom import Custom

with Diagram("Web Application Architecture", show=False):

    vue_frontend = Vue("Vue.js Frontend")
    flask_backend = Flask("Flask Backend")

    with Cluster("API Endpoints"):
        api_cities = Fastapi("/api/cities")
        api_cpt_translations = Fastapi("/api/cpt_translations")
        api_hospital_charges = Fastapi("/api/hospital_charges")
        api_hospitals = Fastapi("/api/hospitals")
        api_payers = Fastapi("/api/payers")
        api_zipcodes = Fastapi("/api/zipcodes")
        api_comprehend_medical = Fastapi("/api/comprehend-medical")

    with Cluster("Database Models"):
        city = SQL("City")
        zipcode = SQL("ZipCode")
        hospital = SQL("Hospital")
        cpt_translation = SQL("CptTranslation")
        hospital_charge = SQL("HospitalCharge")
        icd_cpt_mapping = SQL("IcdCptMapping")
        payer = SQL("Payer")

    # Frontend interactions
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_cities - Edge(color="green") - city
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_cpt_translations - Edge(color="green") - cpt_translation
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_hospital_charges - Edge(color="green") - hospital_charge
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_hospitals - Edge(color="green") - hospital
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_payers - Edge(color="green") - payer
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_zipcodes - Edge(color="green") - zipcode
    vue_frontend - Edge(color="blue", style="dotted") - flask_backend - api_comprehend_medical - Edge(color="red") - [icd_cpt_mapping, hospital_charge]

    # Model relationships
    city - Edge(color="black") - zipcode
    zipcode - Edge(color="black") - hospital
    cpt_translation - Edge(color="purple") - [hospital_charge, icd_cpt_mapping]
    icd_cpt_mapping - Edge(color="purple") - hospital_charge
    payer - Edge(color="orange", style="dashed") - zipcode
