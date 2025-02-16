#!/bin/bash

# Create folder for the script
mkdir -p ~/FolderDocumenter

# Create the Python script
cat > ~/FolderDocumenter/document_folders.py << 'EOL'
#!/usr/bin/env python3

import os
from pathlib import Path
import datetime

print("\n=== Folder Structure Documentation Tool ===\n")
print("This tool will create a report of your folder structure.\n")

# Get the folder path
print("Instructions:")
print("1. Find the folder you want to document in Finder")
print("2. Right-click the folder and hold Option (Alt) key")
print("3. Select 'Copy as Pathname'")
print("4. Paste the path below\n")

folder_path = input("Paste the folder path here: ").strip()

if folder_path.startswith('"') and folder_path.endswith('"'):
    folder_path = folder_path[1:-1]

if not os.path.exists(folder_path):
    print("\nError: Cannot find that folder. Please try again.")
    exit(1)

# Generate report
print("\nCreating report...")

report = []
report.append("Folder Structure Report")
report.append("=====================")
report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append(f"Root Folder: {folder_path}\n")

for root, dirs, files in os.walk(folder_path):
    level = root.replace(folder_path, '').count(os.sep)
    indent = '  ' * level
    folder_name = os.path.basename(root)
    if level == 0:
        folder_name = os.path.basename(folder_path)
    
    report.append(f"{indent}📁 {folder_name}/")
    
    subindent = '  ' * (level + 1)
    for f in sorted(files):
        if not f.startswith('.'):  # Skip hidden files
            report.append(f"{subindent}📄 {f}")

# Save report
desktop_path = os.path.expanduser("~/Desktop")
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
report_name = f"FolderReport_{timestamp}.txt"
report_path = os.path.join(desktop_path, report_name)

with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nDone! Your report has been saved to your Desktop as '{report_name}'")
print("\nPress Enter to exit...")
input()
EOL

# Create the launcher script
cat > ~/FolderDocumenter/Document_Folders.command << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
python3 document_folders.py
EOL

# Make scripts executable
chmod +x ~/FolderDocumenter/document_folders.py
chmod +x ~/FolderDocumenter/Document_Folders.command

# Create shortcut on Desktop
ln -s ~/FolderDocumenter/Document_Folders.command ~/Desktop/Document_Folders

echo "Installation complete! You'll find 'Document_Folders' on your Desktop."

