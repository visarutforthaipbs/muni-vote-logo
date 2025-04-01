import firebase_admin
from firebase_admin import credentials, storage
import os
from pathlib import Path
import mimetypes

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Initialize Firebase Admin SDK with the GCS bucket URI format
        cred = credentials.Certificate('muni-logo-vote-firebase-adminsdk-fbsvc-887cf375c1.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'muni-logo-vote.firebasestorage.app'  # Using the bucket name without gs:// prefix
        })
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Error initializing Firebase: {str(e)}")
        raise

def upload_file(file_path, destination_path):
    """Upload a single file to Firebase Storage"""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(destination_path)
        
        # Set content type
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'image/png'
        
        # Upload the file
        blob.upload_from_filename(
            file_path,
            content_type=content_type
        )
        
        # Make the file publicly accessible
        blob.make_public()
        
        print(f"Successfully uploaded: {destination_path}")
        return blob.public_url
    except Exception as e:
        print(f"Error uploading {file_path}: {str(e)}")
        return None

def main():
    # Initialize Firebase
    initialize_firebase()
    
    # Directory containing the images
    image_dir = Path('municipality_logos')
    
    # Create a list to store upload results
    upload_results = []
    
    # Get all image files
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']:
        image_files.extend(list(image_dir.glob(ext)))
    
    print(f"Found {len(image_files)} images to upload")
    
    # Upload each image
    for image_path in image_files:
        # Get the filename without extension
        filename = image_path.stem
        
        # Create destination path in Firebase Storage
        destination_path = f"municipality_logos/{filename}.png"
        
        # Upload the file
        public_url = upload_file(str(image_path), destination_path)
        
        if public_url:
            upload_results.append({
                'muni_code': filename,
                'url': public_url
            })
    
    # Save upload results to a CSV file
    if upload_results:
        import pandas as pd
        results_df = pd.DataFrame(upload_results)
        results_df.to_csv('upload_results.csv', index=False)
        print("\nUpload results have been saved to 'upload_results.csv'")
    
    print(f"\nUpload Summary:")
    print(f"Successfully uploaded: {len(upload_results)} files")
    print(f"Failed uploads: {len(image_files) - len(upload_results)} files")

if __name__ == "__main__":
    main() 