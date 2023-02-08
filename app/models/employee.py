from app import db
from app.models.utils import ModelMixin


class Employee(db.Model, ModelMixin):
    __tablename__="employees"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(16), nullable=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    birthday = db.Column(db.DateTime(), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    company = db.relationship("Company", back_populates="employees")
    