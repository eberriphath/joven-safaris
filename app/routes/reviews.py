from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.review import Review

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.route("/reviews", methods=["POST"])
def create_review():
    data = request.get_json()
    
    review = Review(
        name=data.get("name"),
        location=data.get("location"),
        rating=data.get("rating"),
        message=data.get("message"),
        approved=False
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "Review submitted successfully.Awaiting approval",
        "review_id":review.id
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

@reviews_bp.route("/admin/reviews", methods=["GET"])
def get_all_reviews():

    reviews = Review.query.order_by(
        Review.created_at.desc()
    ).all()

    return jsonify([
        {
            "id": review.id,
            "name": review.name,
            "location": review.location,
            "rating": review.rating,
            "message": review.message,
            "approved": review.approved
        }
        for review in reviews
    ])

@reviews_bp.route("/admin/reviews/<int:review_id>/approve", methods=["PUT"])
def approve_review(review_id):

    review = Review.query.get_or_404(review_id)

    review.approved = True

    db.session.commit()

    return jsonify({
        "message": "Review approved successfully"
    })

