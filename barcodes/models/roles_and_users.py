from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required


from barcodes.baseapp import app, db


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


user_data_store = MongoEngineUserDatastore(db, user_model=User, role_model=Role)
security = Security(app, user_data_store)
