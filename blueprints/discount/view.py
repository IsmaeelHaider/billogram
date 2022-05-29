from datetime import datetime

from flask import jsonify, request
import logging

from blueprints.discount import discount_blueprint
from models.models import DiscountVoucher

logger = logging.getLogger(__name__)


@discount_blueprint.route("/code", methods=["GET", "POST"])
def discount_code():
    response = {}
    if request.method == "GET":
        brand_id = request.args.get('brand_id', None)
        user_id = request.args.get('customer_id', None)  # TODO: Should get this id from JWT token but for simplicity I'm just hardcoding it
        if brand_id:
            response = DiscountVoucher.get_new_discount_voucher(user_id=user_id, brand_id=brand_id)
        else:
            response = {"error": "Please provide 'brand_id'"}

    elif request.method == "POST":
        payload = request.json
        total_number_of_codes = payload.pop('total_codes', None)
        if total_number_of_codes:
            response = DiscountVoucher.create_discount_vouchers(payload, total_number_of_codes)
        else:
            response = {"error": "Please provide 'total_codes'"}

    return jsonify(response)
