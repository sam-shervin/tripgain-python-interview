#!/bin/bash
# Quick start setup script for Gemini Integration Project

echo "=== Gemini Integration Setup ==="
echo ""

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Check GEMINI_API_KEY
echo ""
echo "=== API Key Configuration ==="
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠ GEMINI_API_KEY not set"
    echo "Please set it before running the script:"
    echo "  export GEMINI_API_KEY='your-api-key-here'"
else
    echo "✓ GEMINI_API_KEY is set"
fi

echo ""
echo "=== Setup Complete ==="
echo "Run the script with: python tripgain_gemini_analysis.py"
