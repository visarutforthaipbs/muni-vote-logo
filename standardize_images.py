from PIL import Image
import os
from pathlib import Path
import glob

def standardize_image(input_path, output_path, target_size=(200, 200)):
    """
    Standardize an image:
    - Convert to PNG
    - Resize while maintaining aspect ratio
    - Add white background if needed
    - Save with consistent quality
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a white background
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))
            
            # Paste the image on the background
            background.paste(img, mask=img.split()[3])
            
            # Calculate new size maintaining aspect ratio
            ratio = min(target_size[0] / img.size[0], target_size[1] / img.size[1])
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            
            # Resize the image
            resized = background.resize(new_size, Image.Resampling.LANCZOS)
            
            # Create a new image with the target size and white background
            final = Image.new('RGBA', target_size, (255, 255, 255, 255))
            
            # Calculate position to center the image
            position = ((target_size[0] - new_size[0]) // 2,
                       (target_size[1] - new_size[1]) // 2)
            
            # Paste the resized image
            final.paste(resized, position)
            
            # Save the standardized image
            final.save(output_path, 'PNG', quality=95)
            print(f"Successfully standardized: {os.path.basename(input_path)}")
            
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def main():
    # Create a temporary directory for processing
    temp_dir = Path('temp_standardized')
    temp_dir.mkdir(exist_ok=True)
    
    # Get all image files from the municipality_logos directory
    input_dir = Path('municipality_logos')
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']:
        image_files.extend(glob.glob(str(input_dir / ext)))
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    for image_path in image_files:
        # Create output path with standardized name
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = temp_dir / f"{name_without_ext}.png"
        
        standardize_image(image_path, output_path)
    
    # Replace original files with standardized versions
    for file in temp_dir.glob('*.png'):
        target_path = input_dir / file.name
        file.rename(target_path)
    
    # Remove temporary directory
    temp_dir.rmdir()
    
    print("\nStandardization complete!")
    print(f"All images have been standardized to 200x200 pixels")
    print(f"Images are saved in the '{input_dir}' directory")

if __name__ == "__main__":
    main() 