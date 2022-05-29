from sqlalchemy import inspect

from extensions import db


class ModelMixins:
    @classmethod
    def bulk_save(cls, objs):
        db.session.bulk_save_objects(objs)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
