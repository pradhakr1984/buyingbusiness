#!/usr/bin/env python3
"""
Additional Business Listing Scrapers
Scrapers for BizQuest, LoopNet, DealStream, and BusinessBroker.net
"""

import re
import time
import logging
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from business_scraper import BusinessScraper, BusinessListing

logger = logging.getLogger(__name__)

class BizQuestScraper(BusinessScraper):
    """Scraper for BizQuest.com"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.bizquest.com"
    
    def scrape_listings(self, max_pages: int = 5) -> List[BusinessListing]:
        """Scrape business listings from BizQuest"""
        listings = []
        driver = self.setup_selenium_driver()
        
        try:
            # BizQuest search URL for New York area
            search_url = f"{self.base_url}/businesses-for-sale/new-york/"
            driver.get(search_url)
            
            # Wait for listings to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listing-item"))
            )
            
            for page in range(max_pages):
                logger.info(f"Scraping BizQuest page {page + 1}")
                
                # Find all listing elements
                listing_elements = driver.find_elements(By.CLASS_NAME, "listing-item")
                
                for element in listing_elements:
                    try:
                        listing = self._extract_bizquest_listing(element, driver)
                        if listing and self._meets_criteria(listing):
                            listings.append(listing)
                    except Exception as e:
                        logger.warning(f"Failed to extract BizQuest listing: {e}")
                        continue
                
                # Navigate to next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")
                    if next_button.is_enabled():
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(3)
                    else:
                        break
                except NoSuchElementException:
                    break
        
        except Exception as e:
            logger.error(f"Error scraping BizQuest: {e}")
        
        finally:
            driver.quit()
        
        return listings
    
    def _extract_bizquest_listing(self, element, driver) -> Optional[BusinessListing]:
        """Extract data from a BizQuest listing element"""
        try:
            # Extract basic information
            name_elem = element.find_element(By.CSS_SELECTOR, ".biz-title a")
            name = name_elem.text.strip()
            listing_url = name_elem.get_attribute("href")
            
            # Extract price
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_elem.text.strip()
                price = self.extract_price(price_text)
            except NoSuchElementException:
                price = 0
            
            # Extract location
            try:
                location_elem = element.find_element(By.CSS_SELECTOR, ".location")
                address = location_elem.text.strip()
            except NoSuchElementException:
                address = "Location not specified"
            
            # Get additional details (simplified for demo)
            description = self._get_text_safe(element, ".description")
            industry = self._get_text_safe(element, ".industry")
            
            # Assess business characteristics
            ai_disruptability = self.assess_ai_disruptability(description, industry)
            labor_intensity = self.assess_labor_intensity(description, "")
            visit_frequency = self.determine_visit_frequency(description, industry)
            
            # Calculate distance
            distance = self.location_service.calculate_distance(address)
            
            return BusinessListing(
                name=name,
                address=address,
                price=price,
                earnings_multiple=0.0,  # Would need detailed page scraping
                ownership_structure="unknown",
                visit_frequency=visit_frequency,
                reason_for_sale="not specified",
                ai_disruptability=ai_disruptability,
                labor_intensity=labor_intensity,
                platform="BizQuest",
                listing_url=listing_url,
                distance_miles=distance
            )
            
        except Exception as e:
            logger.warning(f"Failed to extract BizQuest listing data: {e}")
            return None
    
    def _get_text_safe(self, element, selector: str) -> str:
        """Safely extract text from an element"""
        try:
            sub_element = element.find_element(By.CSS_SELECTOR, selector)
            return sub_element.text.strip()
        except NoSuchElementException:
            return ""

class LoopNetScraper(BusinessScraper):
    """Scraper for LoopNet business sales section"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.loopnet.com"
    
    def scrape_listings(self, max_pages: int = 3) -> List[BusinessListing]:
        """Scrape business listings from LoopNet"""
        listings = []
        driver = self.setup_selenium_driver()
        
        try:
            # LoopNet business for sale search in NYC area
            search_url = f"{self.base_url}/search/businesses-for-sale/new-york-ny/"
            driver.get(search_url)
            
            # Wait for listings to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "placard"))
            )
            
            for page in range(max_pages):
                logger.info(f"Scraping LoopNet page {page + 1}")
                
                # Find all listing elements
                listing_elements = driver.find_elements(By.CLASS_NAME, "placard")
                
                for element in listing_elements:
                    try:
                        listing = self._extract_loopnet_listing(element)
                        if listing and self._meets_criteria(listing):
                            listings.append(listing)
                    except Exception as e:
                        logger.warning(f"Failed to extract LoopNet listing: {e}")
                        continue
                
                # Navigate to next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
                    if next_button.is_enabled():
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(3)
                    else:
                        break
                except NoSuchElementException:
                    break
        
        except Exception as e:
            logger.error(f"Error scraping LoopNet: {e}")
        
        finally:
            driver.quit()
        
        return listings
    
    def _extract_loopnet_listing(self, element) -> Optional[BusinessListing]:
        """Extract data from a LoopNet listing element"""
        try:
            # Extract basic information
            name_elem = element.find_element(By.CSS_SELECTOR, ".placard-title a")
            name = name_elem.text.strip()
            listing_url = name_elem.get_attribute("href")
            
            # Extract price
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, ".placard-price")
                price_text = price_elem.text.strip()
                price = self.extract_price(price_text)
            except NoSuchElementException:
                price = 0
            
            # Extract location
            try:
                location_elem = element.find_element(By.CSS_SELECTOR, ".placard-address")
                address = location_elem.text.strip()
            except NoSuchElementException:
                address = "Location not specified"
            
            # Get property type/description
            try:
                description_elem = element.find_element(By.CSS_SELECTOR, ".placard-property-type")
                description = description_elem.text.strip()
            except NoSuchElementException:
                description = ""
            
            # Assess business characteristics
            ai_disruptability = self.assess_ai_disruptability(description, name)
            labor_intensity = self.assess_labor_intensity(description, "")
            visit_frequency = self.determine_visit_frequency(description, name)
            
            # Calculate distance
            distance = self.location_service.calculate_distance(address)
            
            return BusinessListing(
                name=name,
                address=address,
                price=price,
                earnings_multiple=0.0,
                ownership_structure="unknown",
                visit_frequency=visit_frequency,
                reason_for_sale="not specified",
                ai_disruptability=ai_disruptability,
                labor_intensity=labor_intensity,
                platform="LoopNet",
                listing_url=listing_url,
                distance_miles=distance
            )
            
        except Exception as e:
            logger.warning(f"Failed to extract LoopNet listing data: {e}")
            return None

class DealStreamScraper(BusinessScraper):
    """Scraper for DealStream (formerly MergerNetwork)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.dealstream.com"
    
    def scrape_listings(self, max_pages: int = 3) -> List[BusinessListing]:
        """Scrape business listings from DealStream"""
        listings = []
        driver = self.setup_selenium_driver()
        
        try:
            # DealStream search for businesses in New York
            search_url = f"{self.base_url}/businesses-for-sale/New-York"
            driver.get(search_url)
            
            # Wait for listings to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "deal-listing"))
            )
            
            for page in range(max_pages):
                logger.info(f"Scraping DealStream page {page + 1}")
                
                # Find all listing elements
                listing_elements = driver.find_elements(By.CLASS_NAME, "deal-listing")
                
                for element in listing_elements:
                    try:
                        listing = self._extract_dealstream_listing(element)
                        if listing and self._meets_criteria(listing):
                            listings.append(listing)
                    except Exception as e:
                        logger.warning(f"Failed to extract DealStream listing: {e}")
                        continue
                
                # Navigate to next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, ".next-page")
                    if next_button.is_enabled():
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(3)
                    else:
                        break
                except NoSuchElementException:
                    break
        
        except Exception as e:
            logger.error(f"Error scraping DealStream: {e}")
        
        finally:
            driver.quit()
        
        return listings
    
    def _extract_dealstream_listing(self, element) -> Optional[BusinessListing]:
        """Extract data from a DealStream listing element"""
        try:
            # Extract basic information
            name_elem = element.find_element(By.CSS_SELECTOR, ".deal-title a")
            name = name_elem.text.strip()
            listing_url = name_elem.get_attribute("href")
            
            # Extract price
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, ".deal-price")
                price_text = price_elem.text.strip()
                price = self.extract_price(price_text)
            except NoSuchElementException:
                price = 0
            
            # Extract location
            try:
                location_elem = element.find_element(By.CSS_SELECTOR, ".deal-location")
                address = location_elem.text.strip()
            except NoSuchElementException:
                address = "Location not specified"
            
            # Get description
            try:
                description_elem = element.find_element(By.CSS_SELECTOR, ".deal-description")
                description = description_elem.text.strip()
            except NoSuchElementException:
                description = ""
            
            # Assess business characteristics
            ai_disruptability = self.assess_ai_disruptability(description, name)
            labor_intensity = self.assess_labor_intensity(description, "")
            visit_frequency = self.determine_visit_frequency(description, name)
            
            # Calculate distance
            distance = self.location_service.calculate_distance(address)
            
            return BusinessListing(
                name=name,
                address=address,
                price=price,
                earnings_multiple=0.0,
                ownership_structure="unknown",
                visit_frequency=visit_frequency,
                reason_for_sale="not specified",
                ai_disruptability=ai_disruptability,
                labor_intensity=labor_intensity,
                platform="DealStream",
                listing_url=listing_url,
                distance_miles=distance
            )
            
        except Exception as e:
            logger.warning(f"Failed to extract DealStream listing data: {e}")
            return None

class BusinessBrokerNetScraper(BusinessScraper):
    """Scraper for BusinessBroker.net"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.businessbroker.net"
    
    def scrape_listings(self, max_pages: int = 3) -> List[BusinessListing]:
        """Scrape business listings from BusinessBroker.net"""
        listings = []
        
        # Note: This is a simplified implementation
        # BusinessBroker.net often requires more complex navigation
        
        try:
            # Use requests for initial implementation
            search_url = f"{self.base_url}/businesses-for-sale/new-york"
            response = self.session.get(search_url)
            
            if response.status_code == 200:
                # Parse with BeautifulSoup
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find business listing containers
                listing_containers = soup.find_all('div', class_='business-listing')
                
                for container in listing_containers:
                    try:
                        listing = self._extract_businessbroker_listing(container)
                        if listing and self._meets_criteria(listing):
                            listings.append(listing)
                    except Exception as e:
                        logger.warning(f"Failed to extract BusinessBroker.net listing: {e}")
                        continue
            
        except Exception as e:
            logger.error(f"Error scraping BusinessBroker.net: {e}")
        
        return listings
    
    def _extract_businessbroker_listing(self, container) -> Optional[BusinessListing]:
        """Extract data from a BusinessBroker.net listing container"""
        try:
            # Extract basic information
            name_elem = container.find('a', class_='business-title')
            if not name_elem:
                return None
            
            name = name_elem.text.strip()
            listing_url = urljoin(self.base_url, name_elem.get('href', ''))
            
            # Extract price
            price_elem = container.find('span', class_='price')
            if price_elem:
                price_text = price_elem.text.strip()
                price = self.extract_price(price_text)
            else:
                price = 0
            
            # Extract location
            location_elem = container.find('span', class_='location')
            if location_elem:
                address = location_elem.text.strip()
            else:
                address = "Location not specified"
            
            # Get description
            description_elem = container.find('div', class_='description')
            description = description_elem.text.strip() if description_elem else ""
            
            # Assess business characteristics
            ai_disruptability = self.assess_ai_disruptability(description, name)
            labor_intensity = self.assess_labor_intensity(description, "")
            visit_frequency = self.determine_visit_frequency(description, name)
            
            # Calculate distance
            distance = self.location_service.calculate_distance(address)
            
            return BusinessListing(
                name=name,
                address=address,
                price=price,
                earnings_multiple=0.0,
                ownership_structure="unknown",
                visit_frequency=visit_frequency,
                reason_for_sale="not specified",
                ai_disruptability=ai_disruptability,
                labor_intensity=labor_intensity,
                platform="BusinessBroker.net",
                listing_url=listing_url,
                distance_miles=distance
            )
            
        except Exception as e:
            logger.warning(f"Failed to extract BusinessBroker.net listing data: {e}")
            return None
