import os
def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    _, file_extension = os.path.splitext(filename)
    return file_extension.lower() in image_extensions
