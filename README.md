# Daily Business Acquisition Tracker

A comprehensive system for automatically monitoring business-for-sale listings across multiple platforms, filtering for AI-resilient opportunities, and presenting results in a beautiful dashboard.

## 🎯 Overview

This system automates the daily process of:
- Scraping business listings from BizBuySell.com and other platforms
- Filtering based on your specific criteria (price, location, earnings multiple, etc.)
- Deduplicating listings across platforms
- Assessing AI disruption risk and labor intensity
- Generating beautiful HTML dashboards for review

## 📋 Target Criteria

- **Price**: Under $5,000,000 USD
- **Location**: Within 50 miles of 37 Warren Street, New York, NY (10007)
- **Earnings Multiple**: ≤ 5x
- **Reason for Sale**: Retirement or related (succession, aging)
- **Management**: Low labor intensity, minimal onsite presence
- **AI Resilience**: Unlikely to be disrupted by near-term AI

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Chrome browser** (for web scraping)
3. **Internet connection** for accessing business listing websites

### Installation

1. **Install Dependencies**
   ```bash
   cd "/Users/prashantradhakrishnan/Downloads/Coding on Cursor/Buying a business"
   pip install -r requirements.txt
   ```

2. **Make Scripts Executable**
   ```bash
   chmod +x *.py
   ```

### Usage Options

#### Option 1: One-Time Scan
Run a single scan and generate dashboard:
```bash
python3 run_daily_scan.py
```

#### Option 2: Scheduled Daily Scans
Set up automatic daily scans at 9:00 AM:
```bash
python3 schedule_daily_scan.py
```

#### Option 3: Manual Dashboard Generation
Generate dashboard from existing JSON data:
```bash
python3 dashboard_generator.py
```

## 📊 Dashboard Features

The HTML dashboard provides:

- **Visual Summary Cards**: Total opportunities, average price, labor intensity breakdown
- **Interactive Business Cards**: Each opportunity displayed with:
  - Business name and asking price
  - Location and distance from target
  - AI disruption assessment
  - Labor intensity rating
  - Visit frequency requirements
  - Direct link to original listing

- **Smart Filtering Tags**: Visual indicators for applied filters
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Color-Coded Categories**: Easy identification of labor intensity levels

## 📁 File Structure

```
├── Markdown.MD                 # Original specification document
├── requirements.txt           # Python dependencies
├── business_scraper.py        # Core scraping and filtering logic
├── dashboard_generator.py     # HTML dashboard creation
├── run_daily_scan.py         # Single scan execution
├── schedule_daily_scan.py    # Automated daily scheduling
├── README.md                 # This documentation
└── Generated Files:
    ├── business_listings_YYYYMMDD.json    # Daily results (JSON)
    ├── business_listings_YYYYMMDD_dashboard.html  # Daily dashboard
    ├── daily_scan_YYYYMMDD.log           # Scan logs
    └── scheduler.log                      # Scheduler logs
```

## 🔧 Configuration

### Customizing Search Criteria

Edit `business_scraper.py` to modify:

**Target Location** (line ~45):
```python
def _get_target_coordinates(self) -> tuple:
    location = self.geolocator.geocode("YOUR_ADDRESS_HERE")
```

**Price Limit** (line ~380):
```python
if listing.price > 5000000:  # Change this value
```

**Distance Radius** (line ~385):
```python
if listing.distance_miles and listing.distance_miles > 50:  # Change radius
```

**Retirement Keywords** (line ~395):
```python
retirement_keywords = ['retirement', 'retiring', 'succession', 'aging', 'health']
```

### Adding More Platforms

The system is designed to easily add new scrapers. To add a platform:

1. Create a new class inheriting from `BusinessScraper`
2. Implement the `scrape_listings()` method
3. Add the scraper to the `BusinessTracker` initialization

Example structure:
```python
class NewPlatformScraper(BusinessScraper):
    def scrape_listings(self, max_pages: int = 5) -> List[BusinessListing]:
        # Implementation here
        pass
```

## 📈 Monitoring and Logs

### Log Files
- `daily_scan_YYYYMMDD.log`: Detailed scan execution logs
- `scheduler.log`: Automated scheduling logs
- `business_scraper.log`: Core scraper activity logs

### Success Indicators
- JSON files generated daily with timestamp
- HTML dashboards automatically opened in browser
- Log entries showing successful completion

## 🛠 Troubleshooting

### Common Issues

**1. Chrome Driver Issues**
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager
```

**2. Network/Scraping Errors**
- Check internet connection
- Verify target websites are accessible
- Review logs for specific error messages

**3. No Results Found**
- Verify search criteria aren't too restrictive
- Check if target websites have changed their structure
- Review distance calculation accuracy

**4. Dashboard Not Opening**
- Manually open the HTML file in your browser
- Check file permissions
- Verify file path in logs

### Getting Help

1. **Check Logs**: Review the daily scan logs for detailed error information
2. **Verify Dependencies**: Ensure all required packages are installed
3. **Test Components**: Run individual scripts to isolate issues

## 🔒 Important Considerations

### Legal and Ethical Use
- Respect website terms of service
- Implement reasonable delays between requests
- Don't overload target servers
- Use data for personal research only

### Data Privacy
- Generated files contain business information - handle appropriately
- Consider local storage security for sensitive data
- Regularly clean up old log files

### Maintenance
- Monitor for website structure changes
- Update dependencies periodically
- Review and adjust filtering criteria as needed

## 📅 Automation Setup

### macOS/Linux Cron Alternative
Instead of the Python scheduler, you can use system cron:

1. Open crontab: `crontab -e`
2. Add daily 9 AM execution:
   ```
   0 9 * * * cd "/Users/prashantradhakrishnan/Downloads/Coding on Cursor/Buying a business" && python3 run_daily_scan.py
   ```

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start program `python3` with argument `run_daily_scan.py`
5. Start in: `"C:\path\to\your\project\folder"`

## 📞 Support

For questions or issues:
1. Review this README thoroughly
2. Check the generated log files
3. Verify your Python and dependency versions
4. Test individual components in isolation

---

**Happy Business Hunting! 🎯**
