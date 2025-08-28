#!/usr/bin/env python3
"""
Scheduler for Daily Business Acquisition Scans
Sets up automated daily execution of the business scanning process
"""

import schedule
import time
import subprocess
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_scan_job():
    """Execute the daily scan job"""
    logger.info("Starting scheduled business acquisition scan...")
    
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        scan_script = os.path.join(script_dir, 'run_daily_scan.py')
        
        # Run the daily scan script
        result = subprocess.run(
            ['python3', scan_script],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        
        if result.returncode == 0:
            logger.info("Daily scan completed successfully!")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"Daily scan failed with return code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error running scheduled scan: {e}")

def main():
    """Main scheduler function"""
    logger.info("Business Acquisition Scanner Scheduler Started")
    logger.info("Scheduled to run daily at 9:00 AM")
    
    # Schedule the job to run daily at 9:00 AM
    schedule.every().day.at("09:00").do(run_scan_job)
    
    # Also allow manual trigger by running this script
    logger.info("Running initial scan...")
    run_scan_job()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
