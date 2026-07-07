from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.package import Package
from app.utils.auth import admin_required


admin_packages_bp = Blueprint(
    "admin_packages",
    __name__
)


@admin_packages_bp.route("/admin/packages", methods=["GET"])
@admin_required
def get_packages():

    packages = Package.query.order_by(
        Package.created_at.desc()
    ).all()

    return jsonify([
        {
            "id": package.id,
            "title": package.title,
            "destination": package.destination,
            "duration": package.duration,
            "price": package.price,
            "description": package.description,
            "image_url": package.image_url,
            "active": package.active
        }
        for package in packages
    ])


@admin_packages_bp.route("/admin/packages/<int:package_id>", methods=["DELETE"])
@admin_required
def delete_package(package_id):

    package = Package.query.get_or_404(package_id)

    db.session.delete(package)

    db.session.commit()

    return jsonify({
        "message": "Package deleted successfully"
    })   

@admin_packages_bp.route("/admin/packages", methods=["POST"])
@admin_required
def create_package():

    data = request.get_json()

    package = Package(
        title=data.get("title"),
        destination=data.get("destination"),
        duration=data.get("duration"),
        price=data.get("price"),
        description=data.get("description"),
        image_url=data.get("image_url"),
        active=data.get("active", True)
    )

    db.session.add(package)
    db.session.commit()

    return jsonify({
        "message": "Package created successfully",
        "package_id": package.id
    }), 201

@admin_packages_bp.route("/admin/packages/<int:package_id>", methods=["PUT"])
@admin_required
def update_package(package_id):

    package = Package.query.get_or_404(package_id)

    data = request.get_json()

    package.title = data.get(
        "title",
        package.title
    )

    package.destination = data.get(
        "destination",
        package.destination
    )

    package.duration = data.get(
        "duration",
        package.duration
    )

    package.price = data.get(
        "price",
        package.price
    )

    package.description = data.get(
        "description",
        package.description
    )

    package.image_url = data.get(
        "image_url",
        package.image_url
    )

    package.active = data.get(
        "active",
        package.active
    )

    db.session.commit()

    return jsonify({
        "message": "Package updated successfully"
    })