import os
import uuid
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify

@deconstructible
class UniqueFilenameUpload:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # Generate a unique English-friendly filename using UUID and slugify
        filename_base = slugify(os.path.basename(filename).split('.')[0])
        unique_name = f"{uuid.uuid4().hex[:8]}-{filename_base}.{ext}"
        # Construct the final path: self.path/unique_name
        return os.path.join(self.path, unique_name)

# Example usage for Product images
def product_image_upload_path(instance, filename):
    return UniqueFilenameUpload(f'trade/images/{instance.created_at.strftime("%Y/%m/%d")}')(instance, filename)