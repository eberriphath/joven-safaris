import cloudinary.uploader


def upload_image(file):

    result = cloudinary.uploader.upload(
        file,
        folder="joven-safaris"
    )

    return result["secure_url"]