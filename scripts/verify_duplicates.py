from PIL import Image
import os
from pathlib import Path
import json

def compare_images(backup_dir, report_file):
    """Compare original duplicate pairs and show their details"""
    # Load the deduplication report
    with open(report_file, 'r') as f:
        duplicates = json.load(f)
    
    print("Comparing duplicate images from backup:")
    print("-" * 50)
    
    for kept_file, removed_files in duplicates.items():
        kept_path = Path(backup_dir) / kept_file
        
        # Load the kept image
        if kept_path.exists():
            kept_img = Image.open(kept_path)
            kept_size = os.path.getsize(kept_path)
            
            print(f"\nKept file: {kept_file}")
            print(f"Size: {kept_size} bytes")
            print(f"Dimensions: {kept_img.size}")
            print(f"Mode: {kept_img.mode}")
            
            # Compare with each removed duplicate
            for removed_file in removed_files:
                removed_path = Path(backup_dir) / removed_file
                if removed_path.exists():
                    removed_img = Image.open(removed_path)
                    removed_size = os.path.getsize(removed_path)
                    
                    print(f"\nRemoved duplicate: {removed_file}")
                    print(f"Size: {removed_size} bytes")
                    print(f"Dimensions: {removed_img.size}")
                    print(f"Mode: {removed_img.mode}")
                    
                    # Compare pixel data
                    if kept_img.size == removed_img.size and kept_img.mode == removed_img.mode:
                        if list(kept_img.getdata()) == list(removed_img.getdata()):
                            print("✓ Images are pixel-perfect duplicates")
                        else:
                            print("✗ Images have different pixel data")
                    else:
                        print("✗ Images have different dimensions or color modes")
                    
                    removed_img.close()
            
            kept_img.close()
        print("-" * 50)

if __name__ == "__main__":
    backup_dir = "municipality_logos_backup_20250402_005551"
    report_file = "deduplication_report_20250402_005551.json"
    
    if os.path.exists(backup_dir) and os.path.exists(report_file):
        compare_images(backup_dir, report_file)
    else:
        print("Backup directory or report file not found!") 