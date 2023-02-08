from app import db
from app.models.utils import ModelMixin


class Company(db.Model, ModelMixin):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    employees = db.relationship("Employee", back_populates="company")

    def __repr__(self):
        return "<Company(title='%s', location='%s')>" % (
            self.title,
            self.location,)
