import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_date(filename):
    try:
        image = Image.open(filename)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    return value.replace(':', '-').replace(' ', '_')
    except Exception as e:
        print(f"Error reading EXIF data from {filename}: {e}")
    return None

def convert_and_rename_images():
    for filename in os.listdir('.'):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            exif_date = get_exif_date(filename)
            if exif_date:
                new_filename = f"{exif_date}.png"
            else:
                new_filename = f"{os.path.splitext(filename)[0]}.png"
            
            try:
                image = Image.open(filename)
                image.save(new_filename, 'PNG')
                print(f'Converted {filename} to {new_filename}')
            except Exception as e:
                print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    convert_and_rename_images()
