from PIL import Image
import os
from pathlib import Path
import json
import matplotlib.pyplot as plt

def show_duplicate_pairs(backup_dir, report_file):
    """Display duplicate image pairs side by side"""
    # Load the deduplication report
    with open(report_file, 'r') as f:
        duplicates = json.load(f)
    
    for kept_file, removed_files in duplicates.items():
        kept_path = Path(backup_dir) / kept_file
        
        for removed_file in removed_files:
            removed_path = Path(backup_dir) / removed_file
            
            if kept_path.exists() and removed_path.exists():
                # Load both images
                kept_img = Image.open(kept_path)
                removed_img = Image.open(removed_path)
                
                # Create a figure with two subplots side by side
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                
                # Display images
                ax1.imshow(kept_img)
                ax1.set_title(f'Kept: {kept_file}')
                ax1.axis('off')
                
                ax2.imshow(removed_img)
                ax2.set_title(f'Removed: {removed_file}')
                ax2.axis('off')
                
                plt.suptitle('Duplicate Pair Comparison')
                plt.show()
                
                # Close the images
                kept_img.close()
                removed_img.close()
                
                # Wait for user input before showing next pair
                input("Press Enter to see next pair...")
                plt.close()

if __name__ == "__main__":
    backup_dir = "municipality_logos_backup_20250402_005551"
    report_file = "deduplication_report_20250402_005551.json"
    
    if os.path.exists(backup_dir) and os.path.exists(report_file):
        show_duplicate_pairs(backup_dir, report_file)
    else:
        print("Backup directory or report file not found!") 