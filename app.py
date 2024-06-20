from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer, Contact, Opportunity, Interaction
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    num_opportunities = Opportunity.query.count()
    stages = db.session.query(Opportunity.stage, db.func.count(Opportunity.stage)).group_by(Opportunity.stage).all()
    interaction_history = Interaction.query.order_by(Interaction.date.desc()).limit(10).all()
    return render_template('dashboard.html', num_opportunities=num_opportunities, stages=stages, interaction_history=interaction_history)

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'POST':
        data = request.json
        new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'], address=data['address'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Customer added"}), 201
    else:
        customers = Customer.query.all()
        return jsonify([{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone, "address": c.address} for c in customers])

@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone, "address": customer.address})
    elif request.method == 'PUT':
        data = request.json
        customer.name = data['name']
        customer.email = data['email']
        customer.phone = data['phone']
        customer.address = data['address']
        db.session.commit()
        return jsonify({"message": "Customer updated"})
    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted"})

@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if request.method == 'POST':
        data = request.json
        new_contact = Contact(name=data['name'], email=data['email'], phone=data['phone'], customer_id=data['customer_id'])
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact added"}), 201
    else:
        contacts = Contact.query.all()
        return jsonify([{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone, "customer_id": c.customer_id} for c in contacts])

@app.route('/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def contact_detail(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({"id": contact.id, "name": contact.name, "email": contact.email, "phone": contact.phone, "customer_id": contact.customer_id})
    elif request.method == 'PUT':
        data = request.json
        contact.name = data['name']
        contact.email = data['email']
        contact.phone = data['phone']
        contact.customer_id = data['customer_id']
        db.session.commit()
        return jsonify({"message": "Contact updated"})
    elif request.method == 'DELETE':
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Contact deleted"})

@app.route('/opportunities', methods=['GET', 'POST'])
def manage_opportunities():
    if request.method == 'POST':
        data = request.json
        new_opportunity = Opportunity(description=data['description'], stage=data['stage'], customer_id=data['customer_id'])
        db.session.add(new_opportunity)
        db.session.commit()
        return jsonify({"message": "Opportunity added"}), 201
    else:
        opportunities = Opportunity.query.all()
        return jsonify([{"id": o.id, "description": o.description, "stage": o.stage, "customer_id": o.customer_id} for o in opportunities])

@app.route('/opportunities/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def opportunity_detail(id):
    opportunity = Opportunity.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({"id": opportunity.id, "description": opportunity.description, "stage": opportunity.stage, "customer_id": opportunity.customer_id})
    elif request.method == 'PUT':
        data = request.json
        opportunity.description = data['description']
        opportunity.stage = data['stage']
        opportunity.customer_id = data['customer_id']
        db.session.commit()
        return jsonify({"message": "Opportunity updated"})
    elif request.method == 'DELETE':
        db.session.delete(opportunity)
        db.session.commit()
        return jsonify({"message": "Opportunity deleted"})

@app.route('/interactions', methods=['GET', 'POST'])
def manage_interactions():
    if request.method == 'POST':
        data = request.json
        new_interaction = Interaction(type=data['type'], date=datetime.fromisoformat(data['date']), notes=data['notes'], customer_id=data['customer_id'])
        db.session.add(new_interaction)
        db.session.commit()
        return jsonify({"message": "Interaction added"}), 201
    else:
        interactions = Interaction.query.all()
        return jsonify([{"id": i.id, "type": i.type, "date": i.date, "notes": i.notes, "customer_id": i.customer_id} for i in interactions])

@app.route('/interactions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def interaction_detail(id):
    interaction = Interaction.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({"id": interaction.id, "type": interaction.type, "date": interaction.date, "notes": interaction.notes, "customer_id": interaction.customer_id})
    elif request.method == 'PUT':
        data = request.json
        interaction.type = data['type']
        interaction.date = datetime.fromisoformat(data['date'])
        interaction.notes = data['notes']
        interaction.customer_id = data['customer_id']
        db.session.commit()
        return jsonify({"message": "Interaction updated"})
    elif request.method == 'DELETE':
        db.session.delete(interaction)
        db.session.commit()
        return jsonify({"message": "Interaction deleted"})

if __name__ == '__main__':
    app.run(debug=True)
