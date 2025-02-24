# controllers/placement_controller.py

from models.placement import Placement
from models import db

def record_placement(student_id, company_id, offer_letter):
    placement = Placement(
        student_id=student_id,
        company_id=company_id,
        offer_letter=offer_letter,
        placement_date=db.func.current_date()
    )
    db.session.add(placement)
    db.session.commit()
    return placement

def get_all_placements():
    return Placement.query.all()

def get_placement(placement_id):
    return Placement.query.get(placement_id)
