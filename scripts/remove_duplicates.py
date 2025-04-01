import os
from pathlib import Path
import hashlib
import shutil
import json
from datetime import datetime
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def backup_directory(src_dir, backup_dir):
    """Create a backup of the source directory"""
    if not os.path.exists(backup_dir):
        shutil.copytree(src_dir, backup_dir)
        print(f"Created backup in: {backup_dir}")

def find_and_remove_duplicates(directory):
    """Find and remove duplicate files, keeping track of what was removed"""
    hash_dict = defaultdict(list)
    removed_files = {}
    
    # First pass: Calculate hashes and group files
    for filepath in Path(directory).glob('*.png'):
        file_hash = get_file_hash(filepath)
        hash_dict[file_hash].append(filepath)
    
    # Second pass: Remove duplicates
    for file_hash, filepaths in hash_dict.items():
        if len(filepaths) > 1:
            # Keep the first file, remove others
            kept_file = filepaths[0]
            files_to_remove = filepaths[1:]
            
            # Record what we're removing
            removed_files[str(kept_file.name)] = [f.name for f in files_to_remove]
            
            # Remove duplicate files
            for filepath in files_to_remove:
                print(f"Removing duplicate: {filepath.name} (duplicate of {kept_file.name})")
                filepath.unlink()
    
    return removed_files

def main():
    # Setup directories
    source_dir = 'municipality_logos'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'municipality_logos_backup_{timestamp}'
    
    print(f"Starting deduplication process...")
    
    # Create backup
    print("\nCreating backup...")
    backup_directory(source_dir, backup_dir)
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    removed_files = find_and_remove_duplicates(source_dir)
    
    # Save removal report
    report_file = f'deduplication_report_{timestamp}.json'
    with open(report_file, 'w') as f:
        json.dump(removed_files, f, indent=2)
    
    print(f"\nDeduplication complete!")
    print(f"Backup created in: {backup_dir}")
    print(f"Removal report saved to: {report_file}")
    print(f"Number of duplicate sets handled: {len(removed_files)}")

if __name__ == "__main__":
    main() 