from flask import Blueprint, jsonify
from app.extensions import db
from app.models.review import Review

admin_reviews_bp = Blueprint("admin_reviews", __name__)

@admin_reviews_bp.route("/admin/reviews", methods=["GET"])
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

@admin_reviews_bp.route("/admin/reviews/<int:review_id>/approve", methods=["PUT"])
def approve_review(review_id):

    review = Review.query.get_or_404(review_id)

    review.approved = True

    db.session.commit()

    return jsonify({
        "message": "Review approved successfully"
    })
