from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseMixin(object):
    @classmethod
    def get(cls, id):
        return cls.query.get(int(id))

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create(cls, **kwargs):
        new = cls(**kwargs)
        db.session.add(new)
        return new

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
