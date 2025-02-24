# models/placement.py

from . import db

class Placement(db.Model):
    __tablename__ = 'placements'
    placement_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    offer_letter = db.Column(db.Text)
    placement_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'placement_id': self.placement_id,
            'student_id': self.student_id,
            'company_id': self.company_id,
            'offer_letter': self.offer_letter,
            'placement_date': self.placement_date
        }
