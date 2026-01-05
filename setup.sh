#!/bin/bash
# Setup script for Asana Seed Data Generator
# This script prepares the environment for running the generator

echo "=================================================="
echo "Asana Seed Data Generator - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Found Python $PYTHON_VERSION"
else
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if Python version is 3.7 or higher
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Python 3.7 or higher is required. Found Python $PYTHON_MAJOR.$PYTHON_MINOR"
    exit 1
fi

echo "✓ Python version check passed"
echo ""

# Install dependencies (none required, but run pip install anyway)
echo "Installing dependencies..."
echo "✓ No external dependencies required (uses Python standard library only)"
echo ""

# Create output directory
echo "Creating output directory..."
mkdir -p output
echo "✓ Output directory created"
echo ""

# Verify config file exists
if [ ! -f "config.ini" ]; then
    echo "⚠️  Warning: config.ini not found. Default values will be used."
    echo "   You can create config.ini to customize generation parameters."
else
    echo "✓ Found config.ini"
fi
echo ""

# Verify schema file exists
if [ ! -f "schema.sql" ]; then
    echo "❌ Error: schema.sql not found. This file is required."
    exit 1
else
    echo "✓ Found schema.sql"
fi
echo ""

echo "=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "To generate the database, run:"
echo "  python3 -m src.main"
echo ""
echo "To verify the generated database, run:"
echo "  python3 verify.py"
echo ""
echo "To customize generation parameters, edit config.ini"
echo ""
