from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
# Use SQLite as fallback if MySQL connection fails
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medingen.db'
# Uncomment and update with your actual MySQL credentials when ready
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_actual_password@localhost/medingen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'medingen-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    usage = db.Column(db.Text, nullable=True)
    mechanism = db.Column(db.Text, nullable=True)
    side_effects = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    chemical_composition = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)

class GenericAlternative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.String(20), nullable=True)  # "In Stock", "Available"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=True)
    category = db.Column(db.String(50), nullable=True)  # Can be null if it's a general FAQ
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

# Database initialization function
def initialize_db():
    try:
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we need to add sample data
        if User.query.count() == 0:
            print("Creating default user: admin/password")
            # Add sample user
            sample_user = User(
                username="admin",
                password=generate_password_hash("password")
            )
            db.session.add(sample_user)
            
            # Add sample medicine
            sample_medicine = Medicine(
                name="UDILIV 300MG TABLET 15'S",
                description="UDILIV 300MG TABLET 15'S is a medication used to treat liver conditions. It contains ursodeoxycholic acid as its active ingredient. It has been used for several decades as a therapeutic agent to manage various liver disorders. UDCA's principal therapeutic effects are due to its properties as a hydrophilic bile acid, which plays a vital role in the treatment of cholestasis, improving bile flow, and exerting anti-inflammatory effects, thereby promoting liver health.",
                usage="Helps in dissolving gallstones\nHelps in treating primary biliary cholangitis (PBC)\nAids in managing other cholestatic liver disorders\nAssists in preventing liver failure\nHelps in improving liver function",
                mechanism="The way UDILIV 300MG TABLET 15'S works for children depends on the condition being treated. It's typically prescribed by a pediatrician or gastroenterologist and will determine the appropriate dosage.\n\nFor adults, UDILIV 300MG TABLET 15'S replaces toxic bile acids with non-toxic ursodeoxycholic acid, which increases bile flow and reduces liver damage. In children, the treatment approach and dosage may vary due to their smaller physique, differing metabolic rates, and potential differences in how to take drugs. In the treatment of primary biliary cholangitis (PBC), the application dose ranges from 13-15 mg/kg of body weight per day, also divided into multiple doses. However, dosages may differ based on individual patient characteristics, severity of the condition, and response to treatment.\n\nThis information is intended to provide general understanding and should not be taken as medical advice. Always consult a healthcare professional.",
                side_effects="Nausea, Abdominal discomfort, Diarrhea, Itching, Hair loss (rare)",
                price=36.00,
                rating=4.3,
                manufacturer="Zydus Pharmaceuticals",
                chemical_composition="Ursodeoxycholic Acid 300mg",
                image_url="/assets/tablet.jpg"
            )
            db.session.add(sample_medicine)
            
            try:
                # Commit to get the medicine ID
                db.session.commit()
                
                # Add generic alternatives
                for i in range(4):
                    alternative = GenericAlternative(
                        medicine_id=sample_medicine.id,
                        name=f"Dolo 650 mg",
                        price=36.00,
                        discount=15,
                        rating=4.3,
                        manufacturer="Micro Labs Limited",
                        image_url="/images/dolo-650.jpg",
                        availability="In Stock" if i % 2 == 0 else "Available"
                    )
                    db.session.add(alternative)
                
                # Add reviews
                ratings = [5, 3, 4, 5]
                comments = [
                    "The medicine is good if a lot costly when compared with the exact generic medicine",
                    "The medicine is good if a lot costly when compared with the exact generic medicine",
                    "The medicine is good if a lot costly when compared with the exact generic medicine",
                    "The medicine is good if a lot costly when compared with the exact generic medicine"
                ]
                
                for i in range(4):
                    review = Review(
                        medicine_id=sample_medicine.id,
                        user_id=sample_user.id,
                        rating=ratings[i],
                        comment=comments[i]
                    )
                    db.session.add(review)
                
                # Add FAQs
                faq_data = [
                    {
                        "category": "Paracetamol",
                        "question": "What is Paracetamol?",
                        "answer": "Paracetamol is a pain reliever and fever reducer. It is used to treat many conditions such as headache, muscle aches, arthritis, backache, toothaches, colds, and fevers."
                    },
                    {
                        "category": "Paracetamol",
                        "question": "How often should I take Paracetamol?",
                        "answer": "Adults may take 500-1000 mg every 4-6 hours when needed, up to a maximum of 4000 mg per day. Children's doses vary based on age and weight. Always consult your doctor or follow the package instructions for the correct dosage."
                    },
                    {
                        "category": "Paracetamol",
                        "question": "Is Paracetamol safe for children?",
                        "answer": "Paracetamol is generally considered safe for children when used at the recommended dose. However, always consult with a healthcare provider before giving any medication to children, especially those under 2 years of age."
                    },
                    {
                        "category": "Paracetamol",
                        "question": "Can I take Paracetamol with other medicines?",
                        "answer": "Paracetamol can interact with certain medications, including those for liver disease, anti-seizure medications, and blood-thinning medications. Always inform your doctor about all medications you are taking before starting a new one."
                    },
                    {
                        "category": "Paracetamol",
                        "question": "Can I take Paracetamol and Ibuprofen together?",
                        "answer": "Yes, it is generally safe to take paracetamol and ibuprofen together. They work in different ways to reduce pain and fever. However, always consult your doctor if you are not sure."
                    }
                ]
                
                for faq_item in faq_data:
                    faq = FAQ(
                        medicine_id=sample_medicine.id,
                        category=faq_item["category"],
                        question=faq_item["question"],
                        answer=faq_item["answer"]
                    )
                    db.session.add(faq)
                
                db.session.commit()
                print("Sample data added successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding sample data: {e}")
                # Even if sample data fails, ensure the admin user is created
                db.session.add(sample_user)
                db.session.commit()
                print("Created admin user only due to error with sample data")
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise

# Authentication Routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    print(f"Login attempt for: {username}")
    
    # For debugging - remove in production!
    if username == "admin" and password == "password":
        # Fallback for demo purposes - only use during development
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token, "user_id": user.id}), 200
        else:
            return jsonify({"message": "User exists in DB but password hash check failed"}), 401
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "user_id": user.id}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

# Medicine Routes
@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    result = []
    
    for medicine in medicines:
        medicine_data = {
            'id': medicine.id,
            'name': medicine.name,
            'description': medicine.description,
            'price': medicine.price,
            'rating': medicine.rating,
            'image_url': medicine.image_url
        }
        result.append(medicine_data)
    
    return jsonify(result), 200

@app.route('/api/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine_details(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    
    # Format the side effects
    side_effects_list = []
    if medicine.side_effects:
        side_effects_list = [effect.strip() for effect in medicine.side_effects.split(',')]
    
    medicine_data = {
        'id': medicine.id,
        'name': medicine.name,
        'description': medicine.description,
        'usage': medicine.usage,
        'mechanism': medicine.mechanism,
        'side_effects': side_effects_list,
        'price': medicine.price,
        'rating': medicine.rating,
        'manufacturer': medicine.manufacturer,
        'chemical_composition': medicine.chemical_composition,
        'image_url': medicine.image_url
    }
    return jsonify(medicine_data), 200

@app.route('/api/medicines/<int:medicine_id>/alternatives', methods=['GET'])
def get_medicine_alternatives(medicine_id):
    alternatives = GenericAlternative.query.filter_by(medicine_id=medicine_id).all()
    result = []
    
    for alt in alternatives:
        alt_data = {
            'id': alt.id,
            'name': alt.name,
            'price': alt.price,
            'discount': alt.discount,
            'rating': alt.rating,
            'manufacturer': alt.manufacturer,
            'image_url': alt.image_url,
            'availability': alt.availability
        }
        result.append(alt_data)
    
    return jsonify(result), 200

@app.route('/api/medicines/<int:medicine_id>/reviews', methods=['GET'])
def get_medicine_reviews(medicine_id):
    reviews = Review.query.filter_by(medicine_id=medicine_id).all()
    result = []
    
    for review in reviews:
        review_data = {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment
        }
        result.append(review_data)
    
    return jsonify(result), 200

@app.route('/api/medicines/<int:medicine_id>/faqs', methods=['GET'])
def get_medicine_faqs(medicine_id):
    # Get medicine-specific FAQs
    medicine_faqs = FAQ.query.filter_by(medicine_id=medicine_id).all()
    
    # Get general FAQs (with medicine_id = None)
    general_faqs = FAQ.query.filter_by(medicine_id=None, category=request.args.get('category', None)).all()
    
    faqs = medicine_faqs + general_faqs
    result = []
    
    for faq in faqs:
        faq_data = {
            'id': faq.id,
            'category': faq.category,
            'question': faq.question,
            'answer': faq.answer
        }
        result.append(faq_data)
    
    return jsonify(result), 200

if __name__ == '__main__':
    # Initialize the database before running the app
    with app.app_context():
        try:
            initialize_db()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Database initialization error: {e}")
            print("Using SQLite as fallback. To use MySQL:")
            print("1. Make sure MySQL server is running")
            print("2. Create a database named 'medingen'")
            print("3. Update the connection string with correct credentials")
            print("4. Restart the application")
    app.run(debug=True)