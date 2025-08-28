#!/usr/bin/env python3
"""
Daily Business Acquisition Tracker
Scrapes business listings from multiple platforms and generates filtered results
"""

import json
import re
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('business_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BusinessListing:
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

class LocationService:
    """Service for calculating distances from target location"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="business_acquisition_tracker")
        self.target_coords = self._get_target_coordinates()
    
    def _get_target_coordinates(self) -> tuple:
        """Get coordinates for 37 Warren Street, New York, NY 10007"""
        try:
            location = self.geolocator.geocode("37 Warren Street, New York, NY 10007")
            if location:
                return (location.latitude, location.longitude)
            else:
                # Fallback coordinates for Financial District, NYC
                return (40.7112, -74.0055)
        except Exception as e:
            logger.warning(f"Failed to geocode target address: {e}")
            return (40.7112, -74.0055)
    
    def calculate_distance(self, address: str) -> Optional[float]:
        """Calculate distance from target location to given address"""
        try:
            location = self.geolocator.geocode(address)
            if location:
                distance = geodesic(
                    self.target_coords,
                    (location.latitude, location.longitude)
                ).miles
                return round(distance, 1)
        except Exception as e:
            logger.warning(f"Failed to calculate distance for {address}: {e}")
        return None

class BusinessScraper:
    """Base class for business listing scrapers"""
    
    def __init__(self):
        self.location_service = LocationService()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def setup_selenium_driver(self) -> webdriver.Chrome:
        """Setup headless Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        return driver
    
    def extract_price(self, price_text: str) -> int:
        """Extract numeric price from text"""
        if not price_text:
            return 0
        
        # Remove common currency symbols and text
        price_text = re.sub(r'[^\d,.]', '', price_text)
        price_text = price_text.replace(',', '')
        
        try:
            return int(float(price_text))
        except (ValueError, TypeError):
            return 0
    
    def extract_earnings_multiple(self, text: str) -> float:
        """Extract earnings multiple from text"""
        if not text:
            return 0.0
        
        # Look for patterns like "4.2x", "4.2 x", "multiple: 4.2"
        patterns = [
            r'(\d+\.?\d*)\s*x',
            r'multiple[:\s]*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*times'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return 0.0
    
    def assess_ai_disruptability(self, description: str, industry: str) -> str:
        """Assess AI disruption risk based on business description"""
        description_lower = description.lower()
        industry_lower = industry.lower()
        
        high_risk_keywords = [
            'data entry', 'customer service', 'bookkeeping', 'accounting',
            'translation', 'transcription', 'content writing', 'marketing'
        ]
        
        low_risk_keywords = [
            'manufacturing', 'logistics', 'construction', 'plumbing',
            'electrical', 'specialized', 'custom', 'hands-on', 'physical'
        ]
        
        full_text = f"{description_lower} {industry_lower}"
        
        if any(keyword in full_text for keyword in high_risk_keywords):
            return "High risk - involves routine tasks easily automated"
        elif any(keyword in full_text for keyword in low_risk_keywords):
            return "Low risk - requires physical presence or specialized expertise"
        else:
            return "Medium risk - requires further analysis"
    
    def assess_labor_intensity(self, description: str, employee_count: str) -> str:
        """Assess labor intensity based on description and employee count"""
        try:
            emp_count = int(re.search(r'\d+', employee_count or '0').group())
        except (AttributeError, ValueError):
            emp_count = 0
        
        description_lower = description.lower()
        
        high_labor_keywords = [
            'restaurant', 'retail', 'customer service', 'call center',
            'hospitality', 'cleaning', 'maintenance staff'
        ]
        
        low_labor_keywords = [
            'automated', 'technology', 'software', 'equipment rental',
            'self-service', 'online', 'digital'
        ]
        
        if emp_count > 20 or any(keyword in description_lower for keyword in high_labor_keywords):
            return "high"
        elif emp_count < 5 or any(keyword in description_lower for keyword in low_labor_keywords):
            return "low"
        else:
            return "medium"
    
    def determine_visit_frequency(self, description: str, business_type: str) -> str:
        """Determine required visit frequency based on business characteristics"""
        full_text = f"{description.lower()} {business_type.lower()}"
        
        daily_keywords = ['restaurant', 'retail', 'customer service']
        weekly_keywords = ['office', 'consulting', 'services']
        monthly_keywords = ['rental', 'storage', 'equipment', 'property']
        
        if any(keyword in full_text for keyword in daily_keywords):
            return "daily"
        elif any(keyword in full_text for keyword in weekly_keywords):
            return "weekly"
        elif any(keyword in full_text for keyword in monthly_keywords):
            return "monthly"
        else:
            return "weekly"  # Default assumption

class BizBuySellScraper(BusinessScraper):
    """
    Scraper for BizBuySell.com
    
    WARNING: This is a demonstration scraper. For production use:
    1. Check BizBuySell's Terms of Service: https://www.bizbuysell.com/terms-of-use
    2. Respect robots.txt: https://www.bizbuysell.com/robots.txt
    3. Consider using legitimate APIs like Zyla API Hub instead
    4. Implement proper rate limiting and error handling
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bizbuysell.com"
        self.terms_url = "https://www.bizbuysell.com/terms-of-use"
        self.robots_url = "https://www.bizbuysell.com/robots.txt"
    
    def scrape_listings(self, max_pages: int = 5) -> List[BusinessListing]:
        """
        Scrape business listings from BizBuySell
        
        NOTE: This is a demonstration. The actual CSS selectors and page structure
        may be different. You should:
        1. Inspect the actual website structure
        2. Update selectors accordingly
        3. Test thoroughly
        4. Consider using APIs instead
        """
        listings = []
        
        # Check Terms of Service compliance first
        logger.warning("Please ensure you have reviewed BizBuySell's Terms of Service")
        logger.warning(f"Terms: {self.terms_url}")
        logger.warning(f"Robots.txt: {self.robots_url}")
        
        # For demonstration, return empty list with warning
        logger.warning("Scraping disabled in demo mode. Use API integration instead.")
        return []
        
        # The following code is commented out as it's for demonstration only:
        """
        driver = self.setup_selenium_driver()
        
        try:
            # NOTE: Actual URL structure may differ - verify current site structure
            search_url = f"{self.base_url}/businesses-for-sale/New-York/New-York"
            driver.get(search_url)
            
            # NOTE: CSS selectors are examples - inspect actual site for correct ones
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-item"))
            )
            
            for page in range(max_pages):
                logger.info(f"Scraping BizBuySell page {page + 1}")
                
                # Find all listing elements
                listing_elements = driver.find_elements(By.CLASS_NAME, "result-item")
                
                for element in listing_elements:
                    try:
                        listing = self._extract_listing_data(element, driver)
                        if listing and self._meets_criteria(listing):
                            listings.append(listing)
                    except Exception as e:
                        logger.warning(f"Failed to extract listing: {e}")
                        continue
                
                # Navigate to next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                    if next_button.is_enabled():
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(3)
                    else:
                        break
                except NoSuchElementException:
                    break
        
        except Exception as e:
            logger.error(f"Error scraping BizBuySell: {e}")
        
        finally:
            driver.quit()
        
        return listings
    
    def _extract_listing_data(self, element, driver) -> Optional[BusinessListing]:
        """Extract data from a single listing element"""
        try:
            # Extract basic information
            name_elem = element.find_element(By.CSS_SELECTOR, ".listing-title a")
            name = name_elem.text.strip()
            listing_url = name_elem.get_attribute("href")
            
            # Extract price
            price_elem = element.find_element(By.CSS_SELECTOR, ".price")
            price_text = price_elem.text.strip()
            price = self.extract_price(price_text)
            
            # Extract location
            location_elem = element.find_element(By.CSS_SELECTOR, ".location")
            address = location_elem.text.strip()
            
            # Get additional details by visiting the listing page
            current_url = driver.current_url
            driver.get(listing_url)
            time.sleep(2)
            
            # Extract detailed information
            description = self._get_text_safe(driver, ".business-description")
            industry = self._get_text_safe(driver, ".industry")
            reason_for_sale = self._get_text_safe(driver, ".reason-for-sale")
            employee_count = self._get_text_safe(driver, ".employees")
            
            # Calculate earnings multiple (this would need to be extracted from financials)
            earnings_multiple = 0.0  # Placeholder - would need more sophisticated extraction
            
            # Assess business characteristics
            ai_disruptability = self.assess_ai_disruptability(description, industry)
            labor_intensity = self.assess_labor_intensity(description, employee_count)
            visit_frequency = self.determine_visit_frequency(description, industry)
            
            # Calculate distance
            distance = self.location_service.calculate_distance(address)
            
            # Go back to search results
            driver.get(current_url)
            time.sleep(2)
            
            return BusinessListing(
                name=name,
                address=address,
                price=price,
                earnings_multiple=earnings_multiple,
                ownership_structure="unknown",  # Would need specific extraction
                visit_frequency=visit_frequency,
                reason_for_sale=reason_for_sale or "not specified",
                ai_disruptability=ai_disruptability,
                labor_intensity=labor_intensity,
                platform="BizBuySell",
                listing_url=listing_url,
                distance_miles=distance
            )
            
        except Exception as e:
            logger.warning(f"Failed to extract listing data: {e}")
            return None
    
    def _get_text_safe(self, driver, selector: str) -> str:
        """Safely extract text from an element"""
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except NoSuchElementException:
            return ""
    
    def _meets_criteria(self, listing: BusinessListing) -> bool:
        """Check if listing meets the specified criteria"""
        # Price filter
        if listing.price > 5000000:
            return False
        
        # Distance filter
        if listing.distance_miles and listing.distance_miles > 50:
            return False
        
        # Earnings multiple filter (when available)
        if listing.earnings_multiple > 5.0 and listing.earnings_multiple > 0:
            return False
        
        # Reason for sale filter (retirement related)
        retirement_keywords = ['retirement', 'retiring', 'succession', 'aging', 'health']
        reason_lower = listing.reason_for_sale.lower()
        if not any(keyword in reason_lower for keyword in retirement_keywords):
            return False
        
        return True

class BusinessListingDeduplicator:
    """Deduplicates business listings across platforms"""
    
    def __init__(self):
        self.similarity_threshold = 0.8
    
    def deduplicate(self, listings: List[BusinessListing]) -> List[BusinessListing]:
        """Remove duplicate listings based on name and address similarity"""
        unique_listings = []
        seen_businesses = set()
        
        for listing in listings:
            business_key = self._generate_business_key(listing)
            
            if business_key not in seen_businesses:
                unique_listings.append(listing)
                seen_businesses.add(business_key)
            else:
                logger.info(f"Duplicate found: {listing.name} at {listing.address}")
        
        return unique_listings
    
    def _generate_business_key(self, listing: BusinessListing) -> str:
        """Generate a unique key for business identification"""
        # Normalize name and address for comparison
        name_normalized = re.sub(r'[^\w\s]', '', listing.name.lower()).strip()
        address_normalized = re.sub(r'[^\w\s]', '', listing.address.lower()).strip()
        
        # Create a composite key
        return f"{name_normalized}|{address_normalized}"

class BusinessTracker:
    """Main class that orchestrates the business tracking process"""
    
    def __init__(self):
        self.scrapers = [
            BizBuySellScraper()
        ]
        self.deduplicator = BusinessListingDeduplicator()
    
    def run_daily_scan(self) -> Dict[str, Any]:
        """Run the daily business scan across all platforms"""
        logger.info("Starting daily business acquisition scan")
        
        all_listings = []
        
        # Scrape from all platforms
        for scraper in self.scrapers:
            try:
                platform_listings = scraper.scrape_listings()
                all_listings.extend(platform_listings)
                logger.info(f"Found {len(platform_listings)} listings from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error scraping with {scraper.__class__.__name__}: {e}")
        
        # Deduplicate across platforms
        unique_listings = self.deduplicator.deduplicate(all_listings)
        logger.info(f"After deduplication: {len(unique_listings)} unique listings")
        
        # Sort by price (ascending)
        unique_listings.sort(key=lambda x: x.price)
        
        # Generate results
        results = {
            "results": [asdict(listing) for listing in unique_listings],
            "no_matches_reason": "" if unique_listings else "No businesses found matching the specified criteria",
            "scan_date": datetime.now().isoformat(),
            "total_listings_found": len(all_listings),
            "unique_listings": len(unique_listings)
        }
        
        # Save to JSON file
        output_file = f"business_listings_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
        return results

if __name__ == "__main__":
    tracker = BusinessTracker()
    results = tracker.run_daily_scan()
    print(f"Scan completed. Found {len(results['results'])} qualifying businesses.")
