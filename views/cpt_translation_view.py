from flask import jsonify, Blueprint, request
from models.cpt_translation import CptTranslation

cpt_translation_view = Blueprint('cpt_translation_view', __name__)


@cpt_translation_view.route('/api/cpt_translations', methods=['GET'])
def get_cpt_translations():
    cpt_code = request.args.get('cpt_code')
    if cpt_code:
        cpt_translation = CptTranslation.query.filter_by(CPT_Code=cpt_code).first()
        if cpt_translation:
            return jsonify(cpt_translation.Description)
    return jsonify(None)
