import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name="dfnvqgyn1",
    api_key="945634964155354",
    api_secret="5E4F_0Y_X9OiS6qKSNGiNQB4Jf4"
)

folder = "media/products"

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    if os.path.isfile(path) and os.path.getsize(path) > 0:
        print("Uploading:", file)
        cloudinary.uploader.upload(path, folder="products")
    else:
        print("Skipping empty file:", file)

print("Upload complete")