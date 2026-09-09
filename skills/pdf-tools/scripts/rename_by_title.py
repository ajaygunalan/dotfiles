#!/usr/bin/env python3
"""
Script to rename PDF files using Claude to extract proper titles.
Extracts first few pages and uses claude -p to get intelligent title suggestions.
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path
import tempfile

def extract_text_from_pdf(pdf_path, pages=3):
    """Extract text from the first few pages of a PDF."""
    try:
        # Use pdftotext to extract text from first few pages
        cmd = ['pdftotext', '-l', str(pages), pdf_path, '-']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return None

def get_title_from_claude(text_content):
    """Use Claude to extract the proper title from PDF text."""
    if not text_content or len(text_content.strip()) < 10:
        return None
    
    # Limit text to first 2000 characters to avoid token limits
    text_preview = text_content[:2000]
    
    # Create the prompt for Claude
    prompt = f"""Extract the main title from this PDF text. Return ONLY the title, nothing else. If no clear title exists, return UNKNOWN.

Text:
{text_preview}

Title:"""

    try:
        # Use claude command with the prompt - fixed subprocess call
        result = subprocess.run(
            ['claude', '-p', prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Get the response and clean it
            title = result.stdout.strip()
            
            # Take only the first line if multiple lines returned
            title = title.split('\n')[0].strip()
            
            # Remove any quotes that might be around the title
            title = title.strip('"\'')
            
            # If title contains explanation text, it's invalid
            if any(word in title.lower() for word in ['notice', 'cannot', 'appears', 'extraction', 'without']):
                return None
            
            # If Claude returned UNKNOWN or empty, return None
            if title == "UNKNOWN" or not title or len(title) > 200:
                return None
            
            return title
        else:
            print(f"Claude error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("Claude timeout")
        return None
    except FileNotFoundError:
        print("Claude command not found. Make sure 'claude' is installed and in PATH")
        return None
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return None

def clean_filename(title):
    """Convert title to a clean filename."""
    if not title:
        return None
    
    # Remove colons and other problematic characters, replace with underscore
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    
    # Replace multiple spaces or underscores with single underscore
    title = re.sub(r'[\s_]+', '_', title)
    
    # Remove leading/trailing underscores
    title = title.strip('_')
    
    # Convert to lowercase
    title = title.lower()
    
    # Limit length to 100 characters
    if len(title) > 100:
        # Try to cut at a word boundary
        title = title[:100].rsplit('_', 1)[0]
    
    return title

def get_user_approval(old_path, claude_title, text_preview):
    """Get user approval for renaming."""
    print("\n" + "="*80)
    print(f"FILE: {old_path}")
    print("-"*80)
    
    if text_preview:
        print("TEXT PREVIEW (first 500 chars):")
        print(text_preview[:500])
    else:
        print("Could not extract text from PDF")
    
    print("-"*80)
    
    if claude_title:
        print(f"CLAUDE SUGGESTED TITLE: {claude_title}")
        new_filename = clean_filename(claude_title)
        if new_filename:
            print(f"SUGGESTED FILENAME: {new_filename}.pdf")
        else:
            print("Could not create valid filename from title")
            new_filename = None
    else:
        print("Claude could not identify a title")
        new_filename = None
    
    print("-"*80)
    print("OPTIONS:")
    if new_filename:
        print("  1. Accept Claude's suggestion")
    print("  2. Enter custom filename (without .pdf extension)")
    print("  3. Skip this file")
    print("  4. Quit")
    
    while True:
        choice = input("\nYour choice: ").strip()
        
        if choice == '1' and new_filename:
            return new_filename
        elif choice == '2':
            custom = input("Enter new filename (without .pdf): ").strip()
            if custom:
                # Clean the custom filename
                custom = clean_filename(custom)
                if custom:
                    return custom
            print("Invalid filename, please try again")
        elif choice == '3':
            return None
        elif choice == '4':
            return 'QUIT'
        else:
            print(f"Invalid choice. Please enter 2-4" if not new_filename else "Invalid choice. Please enter 1-4")

def main():
    """Main function to process PDFs."""
    # Find all PDF files
    pdf_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    # Sort files for consistent processing
    pdf_files.sort()
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print("Using Claude to intelligently extract titles...")
    print("="*80)
    
    # Track progress
    processed = 0
    renamed = 0
    skipped = 0
    errors = 0
    
    # Process each PDF
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\nProcessing {i}/{len(pdf_files)}: {pdf_path}")
        
        # Extract text from PDF
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            print("Asking Claude to identify the title...")
            # Get title from Claude
            claude_title = get_title_from_claude(text)
        else:
            claude_title = None
            print("Failed to extract text from PDF")
        
        # Get user approval
        new_filename = get_user_approval(pdf_path, claude_title, text)
        
        if new_filename == 'QUIT':
            print("\nQuitting...")
            break
        elif new_filename:
            # Perform rename
            old_path = Path(pdf_path)
            new_path = old_path.parent / f"{new_filename}.pdf"
            
            # Check if target exists
            if new_path.exists() and new_path != old_path:
                print(f"ERROR: Target file already exists: {new_path}")
                errors += 1
            else:
                try:
                    # Check if file is tracked by git
                    git_check = subprocess.run(
                        ['git', 'ls-files', '--error-unmatch', pdf_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    ).returncode
                    
                    if git_check == 0:
                        # Use git mv for tracked files
                        result = subprocess.run(
                            ['git', 'mv', pdf_path, str(new_path)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        if result.returncode == 0:
                            print(f"✓ Renamed (git): {old_path.name} -> {new_path.name}")
                            renamed += 1
                        else:
                            print(f"ERROR: Git rename failed: {result.stderr.decode()}")
                            errors += 1
                    else:
                        # Use regular rename for untracked files
                        old_path.rename(new_path)
                        print(f"✓ Renamed: {old_path.name} -> {new_path.name}")
                        renamed += 1
                    
                except Exception as e:
                    print(f"ERROR: Rename failed: {e}")
                    errors += 1
        else:
            print("Skipped")
            skipped += 1
        
        processed += 1
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY:")
    print(f"  Total files: {len(pdf_files)}")
    print(f"  Processed: {processed}")
    print(f"  Renamed: {renamed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()