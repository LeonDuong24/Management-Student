import cloudinary

def get_image(request):
    img = cloudinary.uploader.upload()
    return img['secure_url']
    