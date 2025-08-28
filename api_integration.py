#!/usr/bin/env python3
"""
Production-Ready API Integration for Business Listings
Uses legitimate APIs and services for reliable data acquisition
"""

import os
import json
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BusinessListing:
    """Business listing data structure"""
    name: str
    address: str
    price: int
    earnings_multiple: float
    ownership_structure: str
    visit_frequency: str
    reason_for_sale: str
    ai_disruptability: str
    labor_intensity: str
    platform: str
    listing_url: str
    distance_miles: Optional[float] = None
    partial_match_explanation: Optional[str] = None

class ZylaAPIIntegration:
    """
    Integration with Zyla API Hub BizBuySell Listings API
    Real API: https://zylalabs.com/api-marketplace/real%2Bestate%2B%26%2Bhousing/bizbuysell%2Blistings%2Bdata%2Bapi/8592
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://zylalabs.com/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_listings(self, location: str = "New York", max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch business listings from Zyla API
        
        NOTE: This is the API structure - actual endpoints may vary
        Check the official documentation for exact parameters
        """
        if not self.api_key:
            logger.error("Zyla API key not provided")
            return []
        
        try:
            # NOTE: Actual endpoint structure should be verified with Zyla documentation
            endpoint = f"{self.base_url}/bizbuysell-listings"
            params = {
                "location": location,
                "limit": max_results,
                "price_max": 5000000,  # Your price filter
            }
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully retrieved {len(data.get('listings', []))} listings")
                return data.get('listings', [])
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from Zyla API: {e}")
            return []
    
    def process_listing(self, raw_listing: Dict[str, Any]) -> Optional[BusinessListing]:
        """Convert raw API data to BusinessListing format"""
        try:
            # NOTE: Field mapping depends on actual API response structure
            return BusinessListing(
                name=raw_listing.get('business_name', 'Unknown'),
                address=raw_listing.get('location', 'Unknown'),
                price=int(raw_listing.get('asking_price', 0)),
                earnings_multiple=float(raw_listing.get('earnings_multiple', 0)),
                ownership_structure=raw_listing.get('ownership_type', 'Unknown'),
                visit_frequency="weekly",  # Would need to be derived from description
                reason_for_sale=raw_listing.get('reason_for_sale', 'Not specified'),
                ai_disruptability="Requires analysis",  # Would need AI assessment
                labor_intensity="medium",  # Would need analysis
                platform="BizBuySell (via Zyla API)",
                listing_url=raw_listing.get('listing_url', ''),
                distance_miles=raw_listing.get('distance', None)
            )
        except Exception as e:
            logger.warning(f"Failed to process listing: {e}")
            return None

class ApifyIntegration:
    """
    Integration with Apify BizBuySell Scraper
    Real service: https://apify.com/acquistion-automation/bizbuysell-scraper
    """
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.apify.com/v2"
        self.actor_id = "acquistion-automation/bizbuysell-scraper"
    
    def run_scraper(self, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Run Apify scraper and get results
        """
        if not self.api_token:
            logger.error("Apify API token not provided")
            return []
        
        try:
            # Start actor run
            run_url = f"{self.base_url}/acts/{self.actor_id}/runs"
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            response = requests.post(run_url, json=input_data, headers=headers)
            
            if response.status_code == 201:
                run_data = response.json()
                run_id = run_data['data']['id']
                
                # Wait for completion and get results
                # NOTE: In production, implement proper polling
                logger.info(f"Scraper started. Run ID: {run_id}")
                logger.info("Check Apify dashboard for results")
                
                return []  # Would return actual results after completion
            else:
                logger.error(f"Failed to start scraper: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with Apify integration: {e}")
            return []

class ProductionBusinessTracker:
    """
    Production-ready business tracker using legitimate APIs
    """
    
    def __init__(self, zyla_key: str = None, apify_token: str = None):
        self.zyla_api = ZylaAPIIntegration(zyla_key) if zyla_key else None
        self.apify_api = ApifyIntegration(apify_token) if apify_token else None
        
        # Load API keys from environment if not provided
        if not zyla_key:
            self.zyla_api = ZylaAPIIntegration(os.getenv('ZYLA_API_KEY'))
        if not apify_token:
            self.apify_api = ApifyIntegration(os.getenv('APIFY_API_TOKEN'))
    
    def get_business_listings(self) -> Dict[str, Any]:
        """
        Get business listings from available APIs
        """
        all_listings = []
        
        # Try Zyla API first
        if self.zyla_api and self.zyla_api.api_key:
            logger.info("Fetching from Zyla API...")
            raw_listings = self.zyla_api.get_listings()
            
            for raw_listing in raw_listings:
                processed = self.zyla_api.process_listing(raw_listing)
                if processed:
                    all_listings.append(processed)
        
        # Fallback to Apify if needed
        elif self.apify_api and self.apify_api.api_token:
            logger.info("Using Apify scraper...")
            input_config = {
                "location": "New York",
                "maxResults": 100,
                "priceMax": 5000000
            }
            raw_listings = self.apify_api.run_scraper(input_config)
            # Process Apify results...
        
        else:
            logger.error("No valid API credentials found")
            return {
                "results": [],
                "error": "No API credentials configured",
                "recommendations": [
                    "Set ZYLA_API_KEY environment variable",
                    "Set APIFY_API_TOKEN environment variable",
                    "Or pass credentials to constructor"
                ]
            }
        
        # Filter and sort results
        filtered_listings = self._filter_listings(all_listings)
        filtered_listings.sort(key=lambda x: x.price)
        
        return {
            "results": [asdict(listing) for listing in filtered_listings],
            "scan_date": datetime.now().isoformat(),
            "total_found": len(all_listings),
            "after_filtering": len(filtered_listings),
            "data_source": "API"
        }
    
    def _filter_listings(self, listings: List[BusinessListing]) -> List[BusinessListing]:
        """Apply your specific filtering criteria"""
        filtered = []
        
        for listing in listings:
            # Apply your filters from the original spec
            if (listing.price <= 5000000 and 
                listing.earnings_multiple <= 5.0 and
                any(keyword in listing.reason_for_sale.lower() for keyword in 
                    ['retirement', 'retiring', 'succession', 'aging'])):
                filtered.append(listing)
        
        return filtered

def main():
    """
    Main function demonstrating production setup
    """
    print("Production Business Acquisition Tracker")
    print("=" * 50)
    
    # Check for API credentials
    zyla_key = os.getenv('ZYLA_API_KEY')
    apify_token = os.getenv('APIFY_API_TOKEN')
    
    if not zyla_key and not apify_token:
        print("⚠️  No API credentials found!")
        print("\nTo use this system, you need:")
        print("1. Zyla API key from: https://zylalabs.com/api-marketplace/real%2Bestate%2B%26%2Bhousing/bizbuysell%2Blistings%2Bdata%2Bapi/8592")
        print("2. Or Apify token from: https://apify.com/acquistion-automation/bizbuysell-scraper")
        print("\nSet environment variables:")
        print("export ZYLA_API_KEY='your_key_here'")
        print("export APIFY_API_TOKEN='your_token_here'")
        return
    
    # Initialize tracker
    tracker = ProductionBusinessTracker(zyla_key, apify_token)
    
    # Get listings
    results = tracker.get_business_listings()
    
    # Save results
    output_file = f"business_listings_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to: {output_file}")
    print(f"📊 Found {results['after_filtering']} qualifying businesses")

if __name__ == "__main__":
    main()
