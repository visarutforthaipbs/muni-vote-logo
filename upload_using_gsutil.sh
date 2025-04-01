#!/bin/bash

# Check if gcloud is installed
if ! command -v gsutil &> /dev/null
then
    echo "gsutil not found. Please install Google Cloud SDK:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the destination bucket
BUCKET="gs://muni-logo-vote.firebasestorage.app"

# Directory containing images
IMAGE_DIR="municipality_logos"

# Log in to gcloud if needed
echo "Checking gcloud authentication..."
gcloud auth login --no-launch-browser

# Log upload results
echo "Starting upload of images to $BUCKET..."
echo "This may take some time depending on the number of images..."

# Upload images
gsutil -m cp -r "$IMAGE_DIR"/*.png "$BUCKET/municipality_logos/"

echo "Upload complete!" 