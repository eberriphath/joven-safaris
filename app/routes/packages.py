from flask import Blueprint, jsonify
from app.models.package import Package


packages_bp = Blueprint(
    "packages",
    __name__
)


@packages_bp.route("/packages", methods=["GET"])
def get_public_packages():

    packages = Package.query.filter_by(
        active=True
    ).all()


    return jsonify([
        {
            "id": package.id,
            "title": package.title,
            "destination": package.destination,
            "duration": package.duration,
            "price": package.price,
            "description": package.description,
            "image_url": package.image_url
        }
        for package in packages
    ])


@packages_bp.route("/packages/<int:id>", methods=["GET"])
def get_single_package(id):

    package = Package.query.get_or_404(id)


    return jsonify({

        "id": package.id,
        "title": package.title,
        "destination": package.destination,
        "duration": package.duration,
        "price": package.price,
        "description": package.description,
        "image_url": package.image_url

    })    