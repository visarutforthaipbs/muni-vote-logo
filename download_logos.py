import pandas as pd
import requests
import os
from urllib.parse import urlparse
import time
from pathlib import Path

# Create a directory to store the images if it doesn't exist
output_dir = Path('municipality_logos')
output_dir.mkdir(exist_ok=True)

# Read the CSV file
df = pd.read_csv('ภาพเทศบาล - check-extracted-data - all-muni-nso-thai.csv')

def get_file_extension(url):
    """Extract file extension from URL or default to .png"""
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        return os.path.splitext(path)[1].lower()
    return '.png'

def download_image(url, muni_code):
    """Download image from URL and save it with municipality code as filename"""
    if pd.isna(url) or url == '':
        print(f"Skipping empty URL for muni_code: {muni_code}")
        return False
    
    try:
        # Add a small delay to be respectful to servers
        time.sleep(0.5)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get file extension from URL or default to .png
        ext = get_file_extension(url)
        filename = f"{muni_code}{ext}"
        filepath = output_dir / filename
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"Error downloading logo for muni_code {muni_code}: {str(e)}")
        return False

# Process each row in the dataframe
successful_downloads = 0
failed_downloads = 0

for index, row in df.iterrows():
    if download_image(row['logo'], row['muni_code']):
        successful_downloads += 1
    else:
        failed_downloads += 1

print(f"\nDownload Summary:")
print(f"Successfully downloaded: {successful_downloads}")
print(f"Failed downloads: {failed_downloads}")
print(f"Images are saved in the '{output_dir}' directory") 