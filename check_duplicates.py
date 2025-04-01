import os
from pathlib import Path
import hashlib
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)  # Read in 64kb chunks
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Find duplicate files based on content"""
    hash_dict = defaultdict(list)
    size_dict = defaultdict(list)
    
    # First, group files by size
    for filepath in Path(directory).glob('*.png'):
        filesize = os.path.getsize(filepath)
        size_dict[filesize].append(filepath)
    
    # Then, for files with same size, check their hashes
    for size, filepaths in size_dict.items():
        if len(filepaths) > 1:  # Only check files that have same size
            for filepath in filepaths:
                file_hash = get_file_hash(filepath)
                hash_dict[file_hash].append(filepath)
    
    return hash_dict

def main():
    directory = 'municipality_logos'
    print(f"Checking for duplicates in {directory}...")
    
    # Find duplicates
    hash_dict = find_duplicates(directory)
    
    # Print results
    found_duplicates = False
    for file_hash, filepaths in hash_dict.items():
        if len(filepaths) > 1:
            found_duplicates = True
            print("\nDuplicate files found:")
            for filepath in filepaths:
                print(f"  - {filepath.name}")
            print(f"File size: {os.path.getsize(filepaths[0])} bytes")
    
    if not found_duplicates:
        print("No duplicate files found!")
    else:
        print("\nTo handle duplicates, you can:")
        print("1. Manually review the files")
        print("2. Keep one copy and delete others")
        print("3. Run a deduplication script")

if __name__ == "__main__":
    main() 