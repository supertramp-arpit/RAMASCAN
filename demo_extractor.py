#!/usr/bin/env python3
"""
Demo script to test the biller image extraction functionality
with a sample HTML page (since paytm.com is not accessible in this environment).
"""

import os
import sys
from extract_biller_images import PaytmBillerImageExtractor
from bs4 import BeautifulSoup

# Sample HTML that simulates a Paytm-like electricity bill payment page
# Note: Using placeholder URLs for demonstration purposes
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Electricity Bill Payment - Sample</title>
</head>
<body>
    <div class="electricity-providers">
        <h2>Select Your Electricity Provider</h2>
        <div class="biller-grid">
            <div class="biller-card">
                <img src="https://cdn.paytm.com/images/tata-power.png" alt="Tata Power Electricity Biller" class="biller-logo">
                <span>Tata Power</span>
            </div>
            <div class="biller-card">
                <img src="https://cdn.paytm.com/images/adani-electricity.png" alt="Adani Electricity Provider" class="operator-logo">
                <span>Adani Electricity</span>
            </div>
            <div class="biller-card">
                <img data-src="https://cdn.paytm.com/images/bses.png" alt="BSES Electricity" class="provider-logo">
                <span>BSES</span>
            </div>
            <div class="biller-card">
                <img src="https://cdn.paytm.com/logos/best.jpg" alt="BEST Mumbai Electricity Operator">
                <span>BEST</span>
            </div>
            <div class="biller-card">
                <img src="https://cdn.paytm.com/electricity/reliance-energy-logo.png" alt="Reliance Energy">
                <span>Reliance Energy</span>
            </div>
        </div>
    </div>
    <div class="other-content">
        <img src="https://cdn.paytm.com/banner.jpg" alt="Advertisement Banner">
    </div>
</body>
</html>
"""


def test_image_parsing():
    """Test the image parsing functionality with sample HTML."""
    print("=" * 60)
    print("Testing Biller Image Extraction")
    print("=" * 60)
    print()
    
    # Create a temporary extractor instance
    extractor = PaytmBillerImageExtractor(
        url='https://paytm.com/electricity-bill-payment/',
        output_dir='test_output'
    )
    
    # Parse the sample HTML
    print("Parsing sample HTML that simulates Paytm electricity page...")
    image_urls = extractor.parse_images(SAMPLE_HTML)
    
    print(f"\nFound {len(image_urls)} biller images:")
    print("-" * 60)
    for i, url in enumerate(image_urls, 1):
        print(f"{i}. {url}")
    
    print()
    print("=" * 60)
    print("Expected results:")
    print("  - Should find 5 biller/provider images")
    print("  - Should NOT include the advertisement banner")
    print("  - Should handle both 'src' and 'data-src' attributes")
    print("=" * 60)
    
    # Analyze the results
    expected_images = [
        'tata-power.png',
        'adani-electricity.png',
        'bses.png',
        'best.jpg',
        'reliance-energy-logo.png'
    ]
    
    found_expected = 0
    for url in image_urls:
        for expected in expected_images:
            if expected in url:
                found_expected += 1
                break
    
    print(f"\nValidation: Found {found_expected} out of {len(expected_images)} expected biller images")
    
    # Check if banner was correctly excluded
    has_banner = any('banner' in url.lower() for url in image_urls)
    print(f"Validation: Advertisement banner correctly excluded: {not has_banner}")
    
    return len(image_urls) > 0


def test_soup_parsing():
    """Test BeautifulSoup parsing capabilities."""
    print("\n" + "=" * 60)
    print("Testing HTML Parsing Strategies")
    print("=" * 60)
    print()
    
    soup = BeautifulSoup(SAMPLE_HTML, 'lxml')
    
    # Test different selectors
    test_selectors = [
        ('img[alt*="biller" i]', 'Images with "biller" in alt text'),
        ('img[alt*="electricity" i]', 'Images with "electricity" in alt text'),
        ('img[class*="biller" i]', 'Images with "biller" in class'),
        ('img[class*="operator" i]', 'Images with "operator" in class'),
        ('img[class*="provider" i]', 'Images with "provider" in class'),
    ]
    
    for selector, description in test_selectors:
        results = soup.select(selector)
        print(f"{description}:")
        print(f"  Selector: {selector}")
        print(f"  Found: {len(results)} images")
        for img in results:
            src = img.get('src') or img.get('data-src', 'N/A')
            alt = img.get('alt', 'N/A')
            print(f"    - {os.path.basename(src)} (alt: {alt})")
        print()
    
    return True


def main():
    """Main demo function."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Paytm Biller Image Extractor - Demo".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Run tests
    test_image_parsing()
    test_soup_parsing()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print()
    print("To use with the actual Paytm website:")
    print("  python extract_biller_images.py")
    print()
    print("Note: This demo uses sample HTML since paytm.com is not")
    print("      accessible in this environment.")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
