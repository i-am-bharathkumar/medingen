from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Medicine, GenericAlternative, Review, FAQ
from flask_cors import CORS  # Import CORS

medicines_bp = Blueprint('medicines', __name__)
CORS(medicines_bp)  # Apply CORS to all routes in this blueprint

@medicines_bp.route('/api/featured-medicine', methods=['GET'])
def get_featured_medicine():
    """
    Get a featured medicine (could be based on most popular, newest, etc.)
    This route is specifically needed for your frontend MedicinePage component
    """
    try:
        # Get the medicine with the highest rating as the featured medicine
        # You could modify this logic based on your business requirements
        featured_medicine = Medicine.query.order_by(Medicine.rating.desc()).first()
        
        if not featured_medicine:
            return jsonify({"message": "No featured medicine found"}), 404
        
        # Format the side effects
        side_effects_list = []
        if featured_medicine.side_effects:
            side_effects_list = [effect.strip() for effect in featured_medicine.side_effects.split(',')]
        
        # Return the medicine data
        medicine_data = {
            'id': featured_medicine.id,
            'name': featured_medicine.name,
            'description': featured_medicine.description,
            'usage': featured_medicine.usage,
            'mechanism': featured_medicine.mechanism,
            'side_effects': side_effects_list,
            'price': featured_medicine.price,
            'rating': featured_medicine.rating,
            'manufacturer': featured_medicine.manufacturer,
            'chemical_composition': featured_medicine.chemical_composition,
            'image_url': featured_medicine.image_url
        }
        
        return jsonify(medicine_data), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching featured medicine: {str(e)}"}), 500

# Your existing routes below
@medicines_bp.route('/', methods=['GET'])
def get_medicines():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    query = Medicine.query
    
    if search:
        query = query.filter(Medicine.name.like(f'%{search}%'))
    
    medicines = query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = {
        'items': [],
        'total': medicines.total,
        'pages': medicines.pages,
        'page': page
    }
    
    for medicine in medicines.items:
        medicine_data = {
            'id': medicine.id,
            'name': medicine.name,
            'description': medicine.description[:100] + '...' if len(medicine.description) > 100 else medicine.description,
            'price': medicine.price,
            'rating': medicine.rating,
            'image_url': medicine.image_url
        }
        result['items'].append(medicine_data)
    
    return jsonify(result), 200

@medicines_bp.route('/<int:medicine_id>', methods=['GET'])
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

@medicines_bp.route('/<int:medicine_id>/alternatives', methods=['GET'])
def get_medicine_alternatives(medicine_id):
    Medicine.query.get_or_404(medicine_id)  # Ensure medicine exists
    
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

@medicines_bp.route('/<int:medicine_id>/reviews', methods=['GET'])
def get_medicine_reviews(medicine_id):
    Medicine.query.get_or_404(medicine_id)  # Ensure medicine exists
    
    reviews = Review.query.filter_by(medicine_id=medicine_id).all()
    result = []
    
    for review in reviews:
        review_data = {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id
        }
        result.append(review_data)
    
    return jsonify(result), 200

@medicines_bp.route('/<int:medicine_id>/reviews', methods=['POST'])
@jwt_required()
def add_medicine_review(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    data = request.get_json()
    user_id = get_jwt_identity()
    
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"message": "Rating must be an integer between 1 and 5"}), 400
    
    new_review = Review(
        medicine_id=medicine_id,
        user_id=user_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    # Update the medicine's average rating
    all_ratings = [r.rating for r in medicine.reviews]
    medicine.rating = sum(all_ratings) / len(all_ratings)
    db.session.commit()
    
    return jsonify({"message": "Review added successfully", "id": new_review.id}), 201

@medicines_bp.route('/<int:medicine_id>/faqs', methods=['GET'])
def get_medicine_faqs(medicine_id):
    Medicine.query.get_or_404(medicine_id)  # Ensure medicine exists
    
    # Get medicine-specific FAQs
    medicine_faqs = FAQ.query.filter_by(medicine_id=medicine_id).all()
    
    # Get general FAQs (with medicine_id = None)
    category = request.args.get('category')
    if category:
        general_faqs = FAQ.query.filter_by(medicine_id=None, category=category).all()
    else:
        general_faqs = FAQ.query.filter_by(medicine_id=None).all()
    
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