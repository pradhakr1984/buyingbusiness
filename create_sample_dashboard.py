#!/usr/bin/env python3
"""
Create Sample Dashboard for Testing and Deployment
This creates a sample HTML dashboard that can be deployed to Vercel
"""

import json
from datetime import datetime
from dashboard_generator import DashboardGenerator

def create_sample_data():
    """Create realistic sample data for testing the dashboard"""
    return {
        "results": [
            {
                "name": "Precision Manufacturing Co.",
                "address": "Long Island City, NY 11101",
                "price": 2750000,
                "earnings_multiple": 4.5,
                "ownership_structure": "50% employee-owned",
                "visit_frequency": "monthly",
                "reason_for_sale": "retirement",
                "ai_disruptability": "Low - specialized CNC machining requires human expertise",
                "labor_intensity": "low",
                "platform": "BizBuySell",
                "listing_url": "https://www.bizbuysell.com/businesses-for-sale/precision-manufacturing-new-york/sample",
                "distance_miles": 12.3,
                "partial_match_explanation": None
            },
            {
                "name": "Commercial Cleaning Services LLC",
                "address": "Jersey City, NJ 07302",
                "price": 1950000,
                "earnings_multiple": 3.8,
                "ownership_structure": "Owner-operated",
                "visit_frequency": "weekly",
                "reason_for_sale": "retirement",
                "ai_disruptability": "Medium - some automation possible but requires on-site presence",
                "labor_intensity": "medium",
                "platform": "BizQuest",
                "listing_url": "https://www.bizquest.com/businesses-for-sale/commercial-cleaning-new-jersey/sample",
                "distance_miles": 8.7,
                "partial_match_explanation": "Visit frequency is weekly rather than monthly"
            },
            {
                "name": "Industrial Equipment Rental",
                "address": "Brooklyn, NY 11232",
                "price": 4200000,
                "earnings_multiple": 4.2,
                "ownership_structure": "Partnership",
                "visit_frequency": "monthly",
                "reason_for_sale": "succession planning",
                "ai_disruptability": "Low - physical equipment management and customer relationships",
                "labor_intensity": "low",
                "platform": "LoopNet",
                "listing_url": "https://www.loopnet.com/listing/industrial-equipment-rental-brooklyn/sample",
                "distance_miles": 18.5,
                "partial_match_explanation": None
            },
            {
                "name": "Specialty Food Distribution",
                "address": "Yonkers, NY 10701",
                "price": 3100000,
                "earnings_multiple": 4.8,
                "ownership_structure": "Family-owned",
                "visit_frequency": "weekly",
                "reason_for_sale": "aging owner",
                "ai_disruptability": "Medium - logistics optimization possible but requires relationship management",
                "labor_intensity": "medium",
                "platform": "DealStream",
                "listing_url": "https://www.dealstream.com/businesses-for-sale/food-distribution-yonkers/sample",
                "distance_miles": 25.2,
                "partial_match_explanation": None
            },
            {
                "name": "HVAC Services & Maintenance",
                "address": "White Plains, NY 10601",
                "price": 1850000,
                "earnings_multiple": 3.5,
                "ownership_structure": "20% employee-owned",
                "visit_frequency": "monthly",
                "reason_for_sale": "retirement",
                "ai_disruptability": "Low - requires skilled technician work and emergency response",
                "labor_intensity": "low",
                "platform": "BusinessBroker.net",
                "listing_url": "https://www.businessbroker.net/businesses-for-sale/hvac-services-white-plains/sample",
                "distance_miles": 31.8,
                "partial_match_explanation": None
            }
        ],
        "scan_date": datetime.now().isoformat(),
        "total_listings_found": 847,
        "unique_listings": 5,
        "no_matches_reason": ""
    }

def main():
    """Create sample dashboard for deployment"""
    print("Creating sample dashboard for deployment...")
    
    # Create sample data
    sample_data = create_sample_data()
    
    # Save sample JSON
    json_filename = "sample_business_listings.json"
    with open(json_filename, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✅ Sample data saved to: {json_filename}")
    
    # Generate dashboard
    generator = DashboardGenerator()
    dashboard_filename = generator.generate_dashboard(
        json_filename, 
        "index.html"  # Use index.html for Vercel deployment
    )
    
    print(f"✅ Dashboard created: {dashboard_filename}")
    print(f"📱 Ready for deployment to Vercel!")
    
    # Also create a dated version for local use
    dated_dashboard = generator.generate_dashboard(
        json_filename,
        f"dashboard_{datetime.now().strftime('%Y%m%d')}.html"
    )
    
    print(f"📊 Local dashboard: {dated_dashboard}")
    print("\nTo view locally, open either file in your browser.")
    print("To deploy to Vercel, push to GitHub with index.html as the main file.")

if __name__ == "__main__":
    main()
