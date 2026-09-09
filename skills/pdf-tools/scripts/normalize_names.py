#!/usr/bin/env python3
"""
Script to rename all files and folders to lowercase with underscores.
Handles git-tracked files properly and preserves directory structure.
"""

import os
import sys
import re
from pathlib import Path

def to_lowercase_underscore(name):
    """Convert a name to lowercase with underscores between words."""
    # Handle common patterns
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)  # camelCase to snake_case
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)  # CAPS to Caps
    name = re.sub(r'\s+', '_', name)  # Replace spaces with underscores
    name = re.sub(r'-', '_', name)  # Replace hyphens with underscores
    name = re.sub(r'[^\w\.]', '_', name)  # Replace special chars with underscores
    name = re.sub(r'_+', '_', name)  # Replace multiple underscores with single
    name = name.strip('_')  # Remove leading/trailing underscores
    return name.lower()

def get_all_paths(root_dir):
    """Get all file and directory paths, excluding .git directory."""
    paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .git directory
        if '.git' in dirpath.split(os.sep):
            continue
        
        # Add directory paths
        for dirname in dirnames:
            if dirname != '.git':
                full_path = os.path.join(dirpath, dirname)
                paths.append(full_path)
        
        # Add file paths
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            paths.append(full_path)
    
    return paths

def get_new_path(old_path):
    """Generate the new path with lowercase and underscores."""
    path_obj = Path(old_path)
    parent = path_obj.parent
    old_name = path_obj.name
    
    # Check if it's a file
    if os.path.isfile(old_path):
        # Get file extension
        extension = path_obj.suffix.lower()
        
        # Skip image files (keep original names)
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico', '.webp', '.tiff'}
        if extension in image_extensions:
            return None
        
        # Only process .md and .pdf files
        allowed_extensions = {'.md', '.pdf'}
        if extension not in allowed_extensions:
            return None
    
    # For directories and allowed files, convert the name
    new_name = to_lowercase_underscore(old_name)
    
    # If it's the same, no change needed
    if old_name == new_name:
        return None
    
    new_path = parent / new_name
    return str(new_path)

def sort_paths_for_renaming(paths):
    """Sort paths so we rename deepest first to avoid conflicts."""
    return sorted(paths, key=lambda p: p.count(os.sep), reverse=True)

def main(dry_run=True):
    """Main function to rename all files and folders."""
    root_dir = os.getcwd()
    print(f"Working directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL RENAMING'}")
    print("-" * 60)
    
    # Get all paths
    all_paths = get_all_paths(root_dir)
    
    # Sort paths (deepest first)
    sorted_paths = sort_paths_for_renaming(all_paths)
    
    # Track renames
    renames = []
    errors = []
    skipped = []
    
    for old_path in sorted_paths:
        new_path = get_new_path(old_path)
        
        if new_path is None:
            skipped.append(old_path)
            continue
        
        # Check if target exists
        if os.path.exists(new_path) and old_path.lower() != new_path.lower():
            errors.append(f"Target exists: {old_path} -> {new_path}")
            continue
        
        renames.append((old_path, new_path))
    
    # Display planned renames
    if renames:
        print(f"\nFiles/folders to rename: {len(renames)}")
        print("-" * 60)
        for old, new in renames[:20]:  # Show first 20
            rel_old = os.path.relpath(old, root_dir)
            rel_new = os.path.relpath(new, root_dir)
            print(f"  {rel_old}")
            print(f"  -> {rel_new}")
        
        if len(renames) > 20:
            print(f"  ... and {len(renames) - 20} more")
    
    # Display errors
    if errors:
        print(f"\nErrors found: {len(errors)}")
        print("-" * 60)
        for error in errors[:10]:
            print(f"  {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    # Display summary
    print(f"\nSummary:")
    print(f"  Total paths scanned: {len(all_paths)}")
    print(f"  To be renamed: {len(renames)}")
    print(f"  Already correct: {len(skipped)}")
    print(f"  Errors: {len(errors)}")
    
    if not dry_run and renames:
        print(f"\nPerforming actual renames...")
        success_count = 0
        fail_count = 0
        
        # Create git mv commands file
        git_commands = []
        
        for old_path, new_path in renames:
            try:
                # Check if file is tracked by git
                git_check = os.system(f'git ls-files --error-unmatch "{old_path}" > /dev/null 2>&1')
                
                if git_check == 0:
                    # File is tracked by git, use git mv
                    result = os.system(f'git mv "{old_path}" "{new_path}"')
                    if result == 0:
                        success_count += 1
                        print(f"  ✓ Renamed (git): {os.path.relpath(old_path, root_dir)}")
                    else:
                        # Fallback to regular rename
                        os.rename(old_path, new_path)
                        git_commands.append(f'git add "{new_path}"')
                        success_count += 1
                        print(f"  ✓ Renamed: {os.path.relpath(old_path, root_dir)}")
                else:
                    # File is not tracked, use regular rename
                    os.rename(old_path, new_path)
                    success_count += 1
                    print(f"  ✓ Renamed: {os.path.relpath(old_path, root_dir)}")
                
            except Exception as e:
                fail_count += 1
                print(f"  ✗ Failed: {os.path.relpath(old_path, root_dir)} - {str(e)}")
        
        print(f"\nRenaming complete!")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {fail_count}")
        
        if git_commands:
            print(f"\nRun these git commands to stage the changes:")
            for cmd in git_commands[:5]:
                print(f"  {cmd}")
            if len(git_commands) > 5:
                print(f"  ... and {len(git_commands) - 5} more")
    
    return len(renames), len(errors)

if __name__ == "__main__":
    # Check for --execute flag
    execute = "--execute" in sys.argv
    
    if not execute:
        print("=" * 60)
        print("DRY RUN MODE - No files will be renamed")
        print("To actually rename files, run: python rename_to_lowercase.py --execute")
        print("=" * 60)
    
    renames, errors = main(dry_run=not execute)
    
    if not execute and renames > 0:
        print("\n" + "=" * 60)
        print("To apply these changes, run:")
        print("  python rename_to_lowercase.py --execute")
        print("=" * 60)