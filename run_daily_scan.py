#!/usr/bin/env python3
"""
Daily Business Acquisition Scanner
Automated script that runs the daily business scan and generates the dashboard
"""

import os
import sys
import logging
import webbrowser
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from business_scraper import BusinessTracker
from dashboard_generator import DashboardGenerator

def setup_logging():
    """Setup logging for the daily scan"""
    log_file = f"daily_scan_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_daily_scan():
    """Run the complete daily business acquisition scan"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("STARTING DAILY BUSINESS ACQUISITION SCAN")
    logger.info("=" * 60)
    
    try:
        # Initialize tracker
        tracker = BusinessTracker()
        
        # Run the scan
        logger.info("Scanning business listings across platforms...")
        results = tracker.run_daily_scan()
        
        # Get the JSON file path
        json_file = f"business_listings_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Generate dashboard
        logger.info("Generating HTML dashboard...")
        generator = DashboardGenerator()
        dashboard_file = generator.generate_dashboard(json_file)
        
        # Convert to absolute path for opening in browser
        dashboard_path = Path(dashboard_file).absolute()
        
        # Log results summary
        logger.info("=" * 60)
        logger.info("SCAN COMPLETE - SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total listings found: {results.get('total_listings_found', 0)}")
        logger.info(f"Unique qualifying businesses: {results.get('unique_listings', 0)}")
        logger.info(f"JSON results saved to: {json_file}")
        logger.info(f"HTML dashboard saved to: {dashboard_file}")
        
        if results.get('results'):
            logger.info("\nTop 3 opportunities by price:")
            for i, business in enumerate(results['results'][:3], 1):
                price_str = f"${business['price']:,}" if business['price'] > 0 else "Price on request"
                logger.info(f"  {i}. {business['name']} - {price_str}")
        
        # Try to open dashboard in browser
        try:
            webbrowser.open(f"file://{dashboard_path}")
            logger.info(f"\nDashboard opened in browser: {dashboard_path}")
        except Exception as e:
            logger.warning(f"Could not open browser automatically: {e}")
            logger.info(f"Please manually open: {dashboard_path}")
        
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"Error during daily scan: {e}")
        logger.error("Check the log file for detailed error information")
        return False

if __name__ == "__main__":
    success = run_daily_scan()
    sys.exit(0 if success else 1)
