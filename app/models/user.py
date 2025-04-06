from ..database import db

ROLE_A = "ROLE_A"
ROLE_B = "ROLE_B"
ROLE_C = "ROLE_C"

# Table d'association entre User et Role
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

# Table d'association entre Token et Role
token_roles = db.Table('token_roles',
    db.Column('token_id', db.Integer, db.ForeignKey('token.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    hashedPwd = db.Column(db.String(256), nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    tokens = db.relationship('Token', backref='user', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    roles = db.relationship('Role', secondary=token_roles, backref=db.backref('tokens', lazy='dynamic'))
