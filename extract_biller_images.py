#!/usr/bin/env python3
"""
Script to extract all biller images from Paytm electricity bill payment page.
URL: https://paytm.com/electricity-bill-payment/

This script will:
1. Fetch the webpage content
2. Parse HTML to find all biller images in the electricity category
3. Download and save images to a local directory
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PaytmBillerImageExtractor:
    """Extract biller images from Paytm electricity bill payment page."""
    
    def __init__(self, url, output_dir='biller_images'):
        """
        Initialize the extractor.
        
        Args:
            url: URL of the Paytm electricity bill payment page
            output_dir: Directory to save downloaded images
        """
        self.url = url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory: {os.path.abspath(self.output_dir)}")
    
    def fetch_page(self):
        """
        Fetch the webpage content.
        
        Returns:
            str: HTML content of the page
        """
        logger.info(f"Fetching page: {self.url}")
        try:
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            logger.info(f"Successfully fetched page (Status: {response.status_code})")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            raise
    
    def parse_images(self, html_content):
        """
        Parse HTML to extract biller image URLs.
        
        Args:
            html_content: HTML content to parse
            
        Returns:
            list: List of image URLs
        """
        logger.info("Parsing HTML to extract image URLs")
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Use a set for O(1) lookup performance
        image_urls_set = set()
        
        # Strategy 1: Find images in common biller container patterns
        # Look for common class names and patterns used for biller icons
        potential_selectors = [
            'img[alt*="biller" i]',
            'img[alt*="electricity" i]',
            'img[src*="biller" i]',
            'img[src*="electricity" i]',
            'img[src*="logo" i]',
            'img[class*="biller" i]',
            'img[class*="operator" i]',
            'img[class*="provider" i]',
            '.biller-logo img',
            '.operator-logo img',
            '.provider-logo img',
            'img[data-src*="biller" i]',
            'img[data-src*="electricity" i]',
        ]
        
        # Find all images using various selectors
        for selector in potential_selectors:
            images = soup.select(selector)
            for img in images:
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if src:
                    full_url = urljoin(self.url, src)
                    if full_url not in image_urls_set:
                        image_urls_set.add(full_url)
                        logger.debug(f"Found image: {full_url}")
        
        # Strategy 2: Find all images and filter by likely biller image patterns
        keywords = ['biller', 'electricity', 'provider', 'operator', 'logo', 'icon']
        all_images = soup.find_all('img')
        for img in all_images:
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if not src:
                continue
            
            # Pre-compute the combined search string
            alt = img.get('alt', '').lower()
            class_name = ' '.join(img.get('class', [])).lower()
            search_text = src.lower() + alt + class_name
            
            # Check if image is likely a biller/provider logo
            if any(keyword in search_text for keyword in keywords):
                full_url = urljoin(self.url, src)
                if full_url not in image_urls_set:
                    image_urls_set.add(full_url)
                    logger.debug(f"Found image (pattern match): {full_url}")
        
        # Convert set to list for return
        image_urls = list(image_urls_set)
        logger.info(f"Found {len(image_urls)} unique image URLs")
        return image_urls
    
    def download_image(self, image_url, index):
        """
        Download a single image.
        
        Args:
            image_url: URL of the image to download
            index: Index number for the image filename
            
        Returns:
            str: Path to the downloaded image or None if failed
        """
        try:
            # Parse URL to get filename
            parsed_url = urlparse(image_url)
            original_filename = os.path.basename(parsed_url.path)
            
            # Get file extension
            ext = os.path.splitext(original_filename)[1]
            if not ext or ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                ext = '.jpg'  # Default extension
            
            # Create filename
            filename = f"biller_{index:03d}{ext}"
            filepath = os.path.join(self.output_dir, filename)
            
            # Download image
            logger.info(f"Downloading image {index}: {image_url}")
            response = self.session.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Saved image to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading image {image_url}: {e}")
            return None
    
    def extract_all_images(self):
        """
        Main method to extract and download all biller images.
        
        Returns:
            list: List of paths to downloaded images
        """
        logger.info("Starting biller image extraction")
        
        # Fetch page
        html_content = self.fetch_page()
        
        # Parse images
        image_urls = self.parse_images(html_content)
        
        if not image_urls:
            logger.warning("No images found on the page")
            return []
        
        # Download images
        downloaded_images = []
        for index, image_url in enumerate(image_urls, start=1):
            filepath = self.download_image(image_url, index)
            if filepath:
                downloaded_images.append(filepath)
            
            # Be respectful to the server
            time.sleep(0.5)
        
        logger.info(f"Successfully downloaded {len(downloaded_images)} out of {len(image_urls)} images")
        return downloaded_images


def main():
    """Main entry point for the script."""
    # URL to scrape
    url = 'https://paytm.com/electricity-bill-payment/'
    
    # Output directory for images
    output_dir = 'electricity_biller_images'
    
    # Create extractor instance
    extractor = PaytmBillerImageExtractor(url, output_dir)
    
    try:
        # Extract and download images
        downloaded_images = extractor.extract_all_images()
        
        # Print summary
        print("\n" + "="*60)
        print(f"Extraction complete!")
        print(f"Total images downloaded: {len(downloaded_images)}")
        print(f"Images saved to: {os.path.abspath(output_dir)}")
        print("="*60)
        
        # List downloaded images
        if downloaded_images:
            print("\nDownloaded images:")
            for img_path in downloaded_images:
                print(f"  - {img_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
