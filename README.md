# RAMASCAN - Paytm Biller Image Extractor

This repository contains a script to extract all biller images from the Paytm electricity bill payment page.

## Description

The `extract_biller_images.py` script scrapes the Paytm electricity bill payment page and downloads all biller/provider logos/images to a local directory.

## Features

- Fetches the Paytm electricity bill payment webpage
- Intelligently identifies and extracts biller images using multiple strategies
- Downloads images with proper error handling
- Saves images with sequential naming for easy organization
- Comprehensive logging for debugging
- Respectful scraping with delays between requests

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4
  - lxml

## Installation

1. Clone this repository:
```bash
git clone https://github.com/supertramp-arpit/RAMASCAN.git
cd RAMASCAN
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Quick Start

Run the main script to extract images from Paytm:

```bash
python extract_biller_images.py
```

### Demo Mode (Test the functionality)

Run the demo script to see how the extraction works with sample HTML:

```bash
python demo_extractor.py
```

This will demonstrate the image extraction logic without requiring access to the actual Paytm website.

### Examples

See various usage examples:

```bash
python examples.py
```

This shows code examples for:
- Basic usage
- Custom output directory
- Fetch and parse only (without downloading)
- Downloading specific images

### Production Mode (Extract from Paytm)

The script will:
1. Fetch the Paytm electricity bill payment page
2. Extract all biller image URLs
3. Download images to the `electricity_biller_images/` directory
4. Display a summary of downloaded images

## Output

Images are saved to the `electricity_biller_images/` directory with filenames:
- `biller_001.jpg`
- `biller_002.png`
- etc.

## Customization

You can modify the script to change:
- **Output directory**: Edit the `output_dir` parameter in the `main()` function
- **URL**: Change the `url` variable to scrape different pages
- **Headers**: Modify the headers in the `__init__()` method of the `PaytmBillerImageExtractor` class

## How It Works

The script uses multiple strategies to identify biller images:

1. **Selector-based search**: Looks for images with specific attributes (alt text, src patterns, class names) related to billers/electricity providers
2. **Pattern matching**: Scans all images on the page and filters based on keywords like "biller", "electricity", "provider", "operator", "logo"
3. **Smart URL parsing**: Handles both regular `src` attributes and lazy-loaded images (`data-src`, `data-lazy-src`)

## Error Handling

The script includes comprehensive error handling:
- Network errors are caught and logged
- Failed image downloads don't stop the entire process
- Detailed logging helps with debugging

## Logging

The script provides detailed logging output:
- INFO: General progress and successful operations
- ERROR: Failed operations with error details
- DEBUG: Detailed information about found images (when logging level is set to DEBUG)

## Security

The script includes several security measures:

- **SSL/TLS Verification**: All HTTPS connections verify SSL certificates by default
- **URL Validation**: Image URLs are validated to prevent SSRF attacks (only http/https schemes allowed)
- **Domain Warnings**: Logs warnings when downloading from external domains
- **Content-Type Detection**: Determines actual file format from HTTP headers to prevent file type confusion
- **Safe File Handling**: Uses proper path construction to prevent directory traversal
- **Error Isolation**: Failed downloads don't crash the entire extraction process

## Notes

- The script is respectful to the server with a 0.5-second delay between image downloads
- Images are downloaded with proper streaming to handle large files efficiently
- The script supports various image formats (JPG, PNG, GIF, WebP, SVG)

## License

This project is open source and available for educational purposes.

## Disclaimer

This script is for educational purposes only. Please ensure you comply with Paytm's terms of service and robots.txt before using this script. Be respectful of server resources and don't overload the server with requests.
