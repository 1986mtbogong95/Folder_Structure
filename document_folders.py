#!/usr/bin/env python3

import os
from pathlib import Path
import datetime
import sys
from typing import List, Tuple

def get_directory_input() -> Path:
    """Prompt user for directory path and validate it."""
    while True:
        dir_path = input("Enter the full path to your project directory: ").strip()
        
        # Handle tilde expansion for home directory
        if dir_path.startswith('~'):
            dir_path = os.path.expanduser(dir_path)
            
        path = Path(dir_path)
        
        if not path.exists():
            print(f"Error: Directory '{dir_path}' does not exist.")
            continue
        if not path.is_dir():
            print(f"Error: '{dir_path}' is not a directory.")
            continue
            
        return path

def analyze_directory(root_path: Path, ignore_patterns: List[str] = None) -> List[Tuple[str, int, int]]:
    """
    Recursively analyze directory structure.
    Returns list of tuples containing (path, file_count, dir_count)
    """
    if ignore_patterns is None:
        ignore_patterns = ['.DS_Store', '.git', '__pycache__', '.pytest_cache']
        
    results = []
    
    for current_path, dirs, files in os.walk(root_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        
        # Filter out ignored files
        files = [f for f in files if f not in ignore_patterns]
        
        rel_path = os.path.relpath(current_path, root_path)
        if rel_path == '.':
            rel_path = os.path.basename(root_path)
            
        results.append((
            rel_path,
            len(files),
            len(dirs)
        ))
        
    return results

def generate_report(root_path: Path, structure: List[Tuple[str, int, int]]) -> str:
    """Generate a formatted report of the directory structure."""
    report = []
    
    # Header
    report.append("Project Directory Structure Report")
    report.append("=" * 35)
    report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Root Directory: {root_path}")
    report.append("\nDirectory Structure:")
    report.append("-" * 35)
    
    # Calculate total statistics
    total_files = sum(item[1] for item in structure)
    total_dirs = sum(item[2] for item in structure)
    
    # Generate tree structure
    for path, file_count, dir_count in structure:
        depth = len(Path(path).parts) - 1
        indent = "  " * depth
        prefix = "└──" if depth > 0 else ""
        
        report.append(f"{indent}{prefix}{os.path.basename(path)}/")
        if file_count > 0 or dir_count > 0:
            stats = []
            if file_count > 0:
                stats.append(f"{file_count} file{'s' if file_count != 1 else ''}")
            if dir_count > 0:
                stats.append(f"{dir_count} dir{'s' if dir_count != 1 else ''}")
            report.append(f"{indent}   ({', '.join(stats)})")
    
    # Add summary
    report.append("\nSummary:")
    report.append("-" * 35)
    report.append(f"Total Directories: {total_dirs}")
    report.append(f"Total Files: {total_files}")
    
    return "\n".join(report)

def main():
    try:
        # Get directory path from user
        root_path = get_directory_input()
        
        # Analyze directory structure
        structure = analyze_directory(root_path)
        
        # Generate and print report
        report = generate_report(root_path, structure)
        print("\n" + report)
        
        # Optionally save report to file
        save = input("\nWould you like to save this report to a file? (y/n): ").lower()
        if save.startswith('y'):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"directory_structure_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            print(f"\nReport saved to: {filename}")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
