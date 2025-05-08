from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

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
    
    alternatives = db.relationship('GenericAlternative', backref='original_medicine', lazy=True)
    reviews = db.relationship('Review', backref='medicine', lazy=True)
    faqs = db.relationship('FAQ', backref='medicine', lazy=True)
    
    def __repr__(self):
        return f'<Medicine {self.name}>'

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
    
    def __repr__(self):
        return f'<GenericAlternative {self.name}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Review {self.id} - Medicine {self.medicine_id}>'

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=True)
    category = db.Column(db.String(50), nullable=True)  # Can be null if it's a general FAQ
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<FAQ {self.id} - {self.question[:20]}...>'