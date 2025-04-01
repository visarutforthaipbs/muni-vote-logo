import firebase_admin
from firebase_admin import credentials, storage
import os
from pathlib import Path

def main():
    try:
        # Initialize Firebase Admin SDK
        print("Initializing Firebase...")
        cred = credentials.Certificate('muni-logo-vote-firebase-adminsdk-fbsvc-887cf375c1.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'muni-logo-vote.firebasestorage.app'
        })
        print("Firebase initialized successfully")
        
        # Get the bucket
        print("Getting bucket...")
        bucket = storage.bucket()
        print(f"Bucket name: {bucket.name}")
        
        # Create a test file if it doesn't exist
        test_file = Path('test_file.txt')
        if not test_file.exists():
            with open(test_file, 'w') as f:
                f.write("This is a test file for Firebase Storage upload.")
            print(f"Created test file: {test_file}")
        
        # Upload the file
        print("Uploading test file...")
        blob = bucket.blob('test_file.txt')
        blob.upload_from_filename(str(test_file))
        
        # Make the file publicly accessible
        blob.make_public()
        print(f"File uploaded successfully. Public URL: {blob.public_url}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 