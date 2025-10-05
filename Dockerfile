# Use slim Python image for better efficiency
FROM python:3.11-slim

# Install only essential system packages for FontForge
RUN apt-get update && apt-get install -y \
    fontforge \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create directories for fonts
WORKDIR /fonts
RUN mkdir -p /fonts/input /fonts/output /fonts/output/ttf /fonts/output/woff /fonts/output/woff2

# Copy OTF fonts and Python conversion script to the container
COPY /input/*.otf /fonts/input/
COPY convert_fonts.py /fonts/

# Make the script executable
RUN chmod +x /fonts/convert_fonts.py

# Set the default command to run the conversion
CMD ["python", "/fonts/convert_fonts.py"]

# Optional: Add a volume mount point for output
VOLUME ["/fonts/output"]