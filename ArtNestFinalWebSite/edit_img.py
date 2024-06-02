from PIL import Image
import os

image_folder = 'img/artistImg/'
# New dimensions
new_size = (445, 542)  # Example: 300x300 pixels

for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.webp')):
        image_path = os.path.join(image_folder, filename)
        with Image.open(image_path) as img:
            # Resize the image and save it
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img.save(image_path)
