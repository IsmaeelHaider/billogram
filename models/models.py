import uuid
from datetime import datetime

from cerberus import Validator
from sqlalchemy.orm import backref

from extensions import db
from models.model_mixins import ModelMixins
from models.validation_schema import discount_code_schema


def generate_uuid():
    return str(uuid.uuid4())


class Brand(db.Model, ModelMixins):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class DiscountVoucher(db.Model, ModelMixins):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    discount_percentage = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship("Brand", backref=backref("brand", uselist=False))
    customer_id = db.Column(db.Integer, nullable=True)

    @classmethod
    def get_new_discount_voucher(cls, brand_id, user_id):
        """
        Create a new voucher and assign it to logged in user.
        :param brand_id:
        :param user_id:
        :return: dict: details of vouchers
        """
        got_discount_already = cls.query.filter_by(customer_id=user_id, brand_id=brand_id).first()

        if got_discount_already:
            return {"error": "Already got discount code"}

        voucher = cls.query.filter(cls.expiry_date > datetime.utcnow()).filter_by(customer_id=None,
                                                                                  is_active=True,
                                                                                  is_used=False,
                                                                                  brand_id=brand_id).first()
        if voucher:
            voucher.customer_id = user_id
            voucher.save()
            voucher_dict = voucher.to_dict()
            voucher_dict['code'] = voucher_dict.pop('id')
            # TODO: Notify brand for new user joined loyalty program using async task like celery.
            return voucher_dict
        else:
            return {"error": "No vouchers available"}

    @staticmethod
    def create_discount_vouchers(payload, total_number_of_codes):
        """
        Responsible to create discount vouchers
        :param payload: voucher config
        :param total_number_of_codes: total number of vouchers to create
        :return: dict
        """
        response = {}

        validator = Validator(discount_code_schema, require_all=True)
        if validator.validate(payload):
            payload['expiry_date'] = datetime.utcfromtimestamp(payload['expiry_date'])
            dvs = [DiscountVoucher(**payload) for i in range(total_number_of_codes)]
            DiscountVoucher.bulk_save(dvs)
            response = {"success": "vouchers created"}
        else:
            response = validator.errors

        return response
