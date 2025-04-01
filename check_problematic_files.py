import os
from pathlib import Path
import mimetypes

def check_file(file_path):
    """Check a file and return information about its status"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return "File does not exist"
        
        # Get file size
        size = os.path.getsize(file_path)
        if size == 0:
            return "File is empty (0 bytes)"
        
        # Get file type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith('image/'):
            return f"File is not an image (MIME type: {mime_type})"
        
        return f"File exists, size: {size} bytes, type: {mime_type}"
        
    except Exception as e:
        return f"Error checking file: {str(e)}"

def main():
    # List of problematic files
    problematic_files = [
        '151986.png',
        '501918.png',
        '571965.png',
        '901954.png',
        '571977.png',
        '301978.png',
        '801991.png',
        '501908.png',
        '501934.png'
    ]
    
    print("Checking problematic files...")
    print("-" * 50)
    
    for filename in problematic_files:
        file_path = Path('municipality_logos') / filename
        status = check_file(file_path)
        print(f"\n{filename}:")
        print(f"Status: {status}")
        
        # If file exists but is problematic, suggest action
        if "File exists" in status:
            print("Suggested action: Try to re-download this file from the original source")
        elif "File does not exist" in status:
            print("Suggested action: This file needs to be downloaded")
        elif "File is empty" in status:
            print("Suggested action: Delete this file and re-download it")
        elif "not an image" in status:
            print("Suggested action: Check if the file extension is correct, re-download if needed")
        
        print("-" * 30)

if __name__ == "__main__":
    main() 