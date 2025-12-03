#!/usr/bin/env python3
"""
Example usage of the Paytm Biller Image Extractor.

This script demonstrates different ways to use the extraction functionality.
"""

from extract_biller_images import PaytmBillerImageExtractor
import sys


def example_basic_usage():
    """Example 1: Basic usage with default settings."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    url = 'https://paytm.com/electricity-bill-payment/'
    extractor = PaytmBillerImageExtractor(url)
    
    try:
        images = extractor.extract_all_images()
        print(f"Downloaded {len(images)} images to 'biller_images/' directory")
    except Exception as e:
        print(f"Error: {e}")


def example_custom_output():
    """Example 2: Custom output directory."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Output Directory")
    print("=" * 60)
    
    url = 'https://paytm.com/electricity-bill-payment/'
    custom_dir = 'my_custom_images'
    
    extractor = PaytmBillerImageExtractor(url, output_dir=custom_dir)
    
    try:
        images = extractor.extract_all_images()
        print(f"Downloaded {len(images)} images to '{custom_dir}/' directory")
    except Exception as e:
        print(f"Error: {e}")


def example_fetch_only():
    """Example 3: Just fetch and parse, don't download."""
    print("\n" + "=" * 60)
    print("Example 3: Fetch and Parse Only (No Download)")
    print("=" * 60)
    
    url = 'https://paytm.com/electricity-bill-payment/'
    extractor = PaytmBillerImageExtractor(url)
    
    try:
        # Fetch page
        html_content = extractor.fetch_page()
        
        # Parse images
        image_urls = extractor.parse_images(html_content)
        
        print(f"Found {len(image_urls)} images:")
        for i, url in enumerate(image_urls, 1):
            print(f"  {i}. {url}")
            
    except Exception as e:
        print(f"Error: {e}")


def example_download_specific():
    """Example 4: Download specific images only."""
    print("\n" + "=" * 60)
    print("Example 4: Download Specific Images")
    print("=" * 60)
    
    url = 'https://paytm.com/electricity-bill-payment/'
    extractor = PaytmBillerImageExtractor(url, output_dir='specific_images')
    
    try:
        # Fetch and parse
        html_content = extractor.fetch_page()
        image_urls = extractor.parse_images(html_content)
        
        # Download only first 3 images (for example)
        print(f"Found {len(image_urls)} images, downloading first 3...")
        for i, img_url in enumerate(image_urls[:3], 1):
            filepath = extractor.download_image(img_url, i)
            if filepath:
                print(f"  Downloaded: {filepath}")
                
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Paytm Biller Image Extractor - Examples".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    print("\nNote: These examples will attempt to connect to paytm.com")
    print("      If the site is not accessible, they will show errors.")
    print()
    
    # Show examples but don't actually run them (to avoid errors)
    print("\n" + "=" * 60)
    print("Available Examples:")
    print("=" * 60)
    print()
    print("1. Basic Usage:")
    print("   url = 'https://paytm.com/electricity-bill-payment/'")
    print("   extractor = PaytmBillerImageExtractor(url)")
    print("   images = extractor.extract_all_images()")
    print()
    
    print("2. Custom Output Directory:")
    print("   extractor = PaytmBillerImageExtractor(url, output_dir='my_images')")
    print("   images = extractor.extract_all_images()")
    print()
    
    print("3. Fetch and Parse Only (no download):")
    print("   html = extractor.fetch_page()")
    print("   image_urls = extractor.parse_images(html)")
    print("   print(image_urls)")
    print()
    
    print("4. Download Specific Images:")
    print("   html = extractor.fetch_page()")
    print("   urls = extractor.parse_images(html)")
    print("   for i, url in enumerate(urls[:3], 1):")
    print("       extractor.download_image(url, i)")
    print()
    
    print("=" * 60)
    print("\nTo run the actual extractor:")
    print("  python extract_biller_images.py")
    print()
    print("To run the demo with sample HTML:")
    print("  python demo_extractor.py")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
