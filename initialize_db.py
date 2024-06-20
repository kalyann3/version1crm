# initialize_db.py

from app import app, db
from models import Customer, Contact, Opportunity, Interaction

# Initialize the Flask app context
with app.app_context():
    # Create all tables
    db.create_all()

print("Database initialized!")