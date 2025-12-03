import os
import uuid
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
from datetime import datetime  # <-- datetime 모듈 추가

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
    
    # ------------------ 수정된 안전장치 로직 ------------------
    date_time_obj = instance.created_at
    
    # created_at이 None인지 확인하고, None이면 현재 시각을 사용
    if date_time_obj is None:
        date_time_obj = datetime.now() 
    # --------------------------------------------------------
    
    # date_time_obj가 None이 아님이 보장된 후 strftime 호출
    path_format = date_time_obj.strftime("%Y/%m/%d")
    
    return UniqueFilenameUpload(f'trade/images/{path_format}')(instance, filename)