from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.review import Review

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/reviews", methods=["POST"])
def create_review():

    data = request.get_json()

    message = data.get("message", "")

    if len(message) > 500:
        return jsonify({
            "error": "Review message cannot exceed 500 characters"
        }), 400

    if len(message.strip()) < 10:
        return jsonify({
            "error": "Review message is too short"
        }), 400


    review = Review(
        name=data.get("name"),
        location=data.get("location"),
        rating=data.get("rating"),
        message=message,
        approved=False
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "Review submitted successfully. Awaiting approval",
        "review_id": review.id
    }), 201

@reviews_bp.route("/reviews", methods=["GET"])
def get_reviews():

    reviews = Review.query.filter_by(approved=True).all()

    return jsonify([
        {
            "id": review.id,
            "name": review.name,
            "location": review.location,
            "rating": review.rating,
            "message": review.message
        }
        for review in reviews
    ])


