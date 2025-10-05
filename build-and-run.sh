#!/bin/bash

# Build and run the font conversion Docker container

echo "Building Docker image..."
docker build -t font-converter .

echo "Running font conversion..."
docker run --name font-converter-temp font-converter

echo "Copying converted fonts to output directory..."
rm -rf output
docker cp font-converter-temp:/fonts/output ./output

echo "Cleaning up temporary container..."
docker rm font-converter-temp

echo ""
echo "✅ Conversion complete! Check the 'output' directory for converted fonts."
echo ""
echo "📁 The output directory contains:"
echo "  - output/ttf/    - TrueType fonts (TTF) - $(find output/ttf -name "*.ttf" 2>/dev/null | wc -l) files"
echo "  - output/woff/   - Web Open Font Format (WOFF) - $(find output/woff -name "*.woff" 2>/dev/null | wc -l) files"
echo "  - output/woff2/  - Web Open Font Format 2 (WOFF2) - $(find output/woff2 -name "*.woff2" 2>/dev/null | wc -l) files"
echo ""
echo "🚀 Ready to use in your web projects!"