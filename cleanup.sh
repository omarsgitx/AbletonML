#!/bin/bash

# AbletonML Project Cleanup Script
# This script removes unnecessary files to reduce the project size

echo "AbletonML Project Cleanup Script"
echo "--------------------------------"

# Remove node_modules (can be reinstalled with npm install)
if [ -d "node_modules" ]; then
  echo "Removing node_modules directory..."
  rm -rf node_modules
  echo "Done. You can reinstall dependencies with 'npm install'"
fi

# Remove __pycache__ directories
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
echo "Done."

# Remove .DS_Store files
echo "Removing .DS_Store files..."
find . -type f -name ".DS_Store" -delete
echo "Done."

# Remove any temporary files
echo "Removing temporary files..."
find . -type f -name "*.tmp" -delete
find . -type f -name "*.log" -delete
echo "Done."

# Remove any git-related files if not needed
read -p "Do you want to remove Git history? (y/n): " remove_git
if [ "$remove_git" = "y" ]; then
  echo "Removing Git history..."
  rm -rf .git
  echo "Done."
fi

echo "--------------------------------"
echo "Cleanup complete!"
echo "To restore the project:"
echo "1. Run 'npm install' to reinstall Node.js dependencies"
echo "2. Run 'pip install -r requirements.txt' to reinstall Python dependencies"
echo "--------------------------------" 