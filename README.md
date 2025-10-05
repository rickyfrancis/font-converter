# Font Converter Docker

This Docker container converts OTF (OpenType) fonts to web-supported formats including TTF, WOFF, and WOFF2.

## Architecture

- **`convert_fonts.py`** - Main Python conversion script (extracted for testability)
- **`Dockerfile`** - Clean, minimal Docker configuration
- **`test_font_converter.py`** - Unit tests for the conversion functions
- **`requirements.txt`** - Python dependencies

## Prerequisites

- Docker installed on your system
- OTF font files in the same directory as the Dockerfile

## Usage

### Quick Start (Windows)

Double-click `build-and-run.bat` or run:

```cmd
build-and-run.bat
```

### Quick Start (Linux/Mac)

Run:

```bash
chmod +x build-and-run.sh
./build-and-run.sh
```

### Manual Usage

1. **Build the Docker image:**

   ```bash
   docker build -t font-converter .
   ```

2. **Run the conversion:**

   ```bash
   docker run --rm -v "$(pwd)/output:/fonts/output" font-converter
   ```

   On Windows:

   ```cmd
   docker run --rm -v "%cd%\output:/fonts/output" font-converter
   ```

## Output

The converted fonts will be saved in the `output` directory with the following structure:

- `output/ttf/` - TrueType fonts (.ttf)
- `output/woff/` - Web Open Font Format (.woff)
- `output/woff2/` - Web Open Font Format 2 (.woff2)

## What the Container Does

1. Copies all `.otf` files from the current directory into the container
2. Converts each OTF font to TTF using FontForge
3. Converts TTF to WOFF using fonttools
4. Converts TTF to WOFF2 using fonttools
5. Outputs all converted fonts to the mounted output directory

## Web Font Usage

After conversion, you can use the fonts in your web projects with CSS:

```css
@font-face {
  font-family: 'PassengerDisplay';
  src: url('fonts/PassengerDisplay-Regular.woff2') format('woff2'), url('fonts/PassengerDisplay-Regular.woff')
      format('woff'),
    url('fonts/PassengerDisplay-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
```

## Supported Input Formats

- OTF (OpenType Font)

## Supported Output Formats

- TTF (TrueType Font) - widely supported, larger file size
- WOFF (Web Open Font Format) - compressed, good browser support
- WOFF2 (Web Open Font Format 2) - better compression, modern browsers
