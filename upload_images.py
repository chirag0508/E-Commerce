import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name="dfnvqgyn1",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

folder = "media/products"

for file in os.listdir(folder):
    path = os.path.join(folder, file)
    if os.path.isfile(path):
        print("Uploading:", file)
        cloudinary.uploader.upload(path, folder="products")

print("Upload complete")