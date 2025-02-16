#!/bin/bash

echo "Installing Folder Documentation Tool..."

# Create the destination directory
mkdir -p ~/FolderDocumenter

# Download the Python script from the repository
curl -o ~/FolderDocumenter/document_folders.py https://raw.githubusercontent.com/1986mtbogong95/Folder_Structure/document_folders.py

# Make it executable
chmod +x ~/FolderDocumenter/document_folders.py

# Create a simple launcher script
cat > ~/FolderDocumenter/Document_Folders.command << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
python3 document_folders.py
EOL

# Make the launcher executable
chmod +x ~/FolderDocumenter/Document_Folders.command

# Create Desktop shortcut
ln -s ~/FolderDocumenter/Document_Folders.command ~/Desktop/Document_Folders

echo "Installation complete! You'll find 'Document_Folders' on your Desktop."
echo "Press Enter to exit..."
read

