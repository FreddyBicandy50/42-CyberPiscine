from PIL import Image
from PIL.ExifTags import TAGS
import sys
import os

def display_metadata(filepath):
    print(f"\nMetadata for: {filepath}")
    try:
        with Image.open(filepath) as img:
            print(f"Format      : {img.format}")
            print(f"Size        : {img.size}")
            print(f"Mode        : {img.mode}")
            print(f"Info        : {img.info}")

            exif_data = img._getexif()
            if exif_data:
                print("\nEXIF Data:")
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name:25}: {value}")
            else:
                print("No EXIF metadata found.")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    for file in sys.argv[1:]:
        if os.path.isfile(file):
            display_metadata(file)
        else:
            print(f"File not found: {file}")
