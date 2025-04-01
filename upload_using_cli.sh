#!/bin/bash

# Create public directory
mkdir -p public/municipality_logos
echo "Created public/municipality_logos directory"

# Copy all images to public directory
cp municipality_logos/*.png public/municipality_logos/
echo "Copied images to public directory"

# Upload to Firebase Storage using Firebase CLI
echo "Deploying to Firebase Storage..."
firebase deploy --only storage

echo "Deployment complete!" 