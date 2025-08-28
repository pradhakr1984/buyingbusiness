#!/usr/bin/env python3
"""
Business Acquisition Dashboard Generator
Creates beautiful HTML dashboards from JSON business listing data
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from jinja2 import Template

class DashboardGenerator:
    """Generates HTML dashboards from business listing JSON data"""
    
    def __init__(self):
        self.template = self._get_html_template()
    
    def generate_dashboard(self, json_file_path: str, output_path: str = None) -> str:
        """Generate HTML dashboard from JSON data file"""
        
        # Load JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Process data for dashboard
        processed_data = self._process_data(data)
        
        # Generate HTML
        html_content = self.template.render(
            data=processed_data,
            generated_time=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            total_listings=len(processed_data['results']),
            scan_date=data.get('scan_date', 'Unknown')
        )
        
        # Save HTML file
        if not output_path:
            base_name = os.path.splitext(os.path.basename(json_file_path))[0]
            output_path = f"{base_name}_dashboard.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw JSON data for dashboard display"""
        results = data.get('results', [])
        
        # Add summary statistics
        if results:
            prices = [r['price'] for r in results if r['price'] > 0]
            avg_price = sum(prices) / len(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            
            # Count by labor intensity
            labor_counts = {'low': 0, 'medium': 0, 'high': 0}
            for result in results:
                labor_intensity = result.get('labor_intensity', 'unknown')
                if labor_intensity in labor_counts:
                    labor_counts[labor_intensity] += 1
            
            # Count by platform
            platform_counts = {}
            for result in results:
                platform = result.get('platform', 'Unknown')
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
        else:
            avg_price = min_price = max_price = 0
            labor_counts = {'low': 0, 'medium': 0, 'high': 0}
            platform_counts = {}
        
        return {
            'results': results,
            'summary': {
                'avg_price': avg_price,
                'min_price': min_price,
                'max_price': max_price,
                'labor_counts': labor_counts,
                'platform_counts': platform_counts
            },
            'no_matches_reason': data.get('no_matches_reason', ''),
            'total_listings_found': data.get('total_listings_found', 0),
            'unique_listings': data.get('unique_listings', 0)
        }
    
    def _get_html_template(self) -> Template:
        """Return the Jinja2 HTML template"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Business Acquisition Tracker - {{ scan_date[:10] }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header .subtitle {
            color: #7f8c8d;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stat-card h3 {
            font-size: 2rem;
            margin-bottom: 5px;
        }
        
        .stat-card p {
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .results-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
        }
        
        .results-header h2 {
            color: #2c3e50;
            font-size: 1.8rem;
        }
        
        .filter-tags {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-tag {
            background: #e74c3c;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .business-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .business-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #3498db;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .business-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }
        
        .business-card.low-labor {
            border-left-color: #27ae60;
        }
        
        .business-card.medium-labor {
            border-left-color: #f39c12;
        }
        
        .business-card.high-labor {
            border-left-color: #e74c3c;
        }
        
        .business-name {
            font-size: 1.3rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.3;
        }
        
        .business-price {
            font-size: 1.8rem;
            font-weight: 700;
            color: #27ae60;
            margin-bottom: 15px;
        }
        
        .business-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .detail-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            border-left: 3px solid #3498db;
        }
        
        .detail-label {
            font-size: 0.8rem;
            color: #7f8c8d;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .business-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .tag {
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .tag.labor-low {
            background: #d5f4e6;
            color: #27ae60;
        }
        
        .tag.labor-medium {
            background: #ffeaa7;
            color: #e17055;
        }
        
        .tag.labor-high {
            background: #ffb3ba;
            color: #e74c3c;
        }
        
        .tag.ai-risk {
            background: #ddd6fe;
            color: #7c3aed;
        }
        
        .ai-assessment {
            background: #f1f3f4;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-style: italic;
            color: #5f6368;
            border-left: 3px solid #9c27b0;
        }
        
        .business-link {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .business-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        .no-results h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9rem;
        }
        
        .platform-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .business-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .business-details {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Daily Business Acquisition Tracker</h1>
            <p class="subtitle">AI-resilient, remotely manageable businesses within 50 miles of 37 Warren Street, NYC</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>{{ total_listings }}</h3>
                    <p>Qualifying Businesses</p>
                </div>
                <div class="stat-card">
                    <h3>${{ "%.1f"|format(data.summary.avg_price / 1000000) }}M</h3>
                    <p>Average Price</p>
                </div>
                <div class="stat-card">
                    <h3>{{ data.summary.labor_counts.low }}</h3>
                    <p>Low Labor Intensity</p>
                </div>
                <div class="stat-card">
                    <h3>{{ data.total_listings_found - data.unique_listings }}</h3>
                    <p>Duplicates Filtered</p>
                </div>
            </div>
        </div>
        
        <div class="results-section">
            <div class="results-header">
                <h2>🎯 Qualifying Opportunities</h2>
                <div class="filter-tags">
                    <span class="filter-tag">Price &lt; $5M</span>
                    <span class="filter-tag">Multiple ≤ 5x</span>
                    <span class="filter-tag">Retirement Sale</span>
                    <span class="filter-tag">50 Mile Radius</span>
                </div>
            </div>
            
            {% if data.results %}
                <div class="business-grid">
                    {% for business in data.results %}
                    <div class="business-card {{ business.labor_intensity }}-labor">
                        <div class="platform-badge">{{ business.platform }}</div>
                        
                        <div class="business-name">{{ business.name }}</div>
                        <div class="business-price">
                            {% if business.price > 0 %}
                                ${{ "{:,.0f}".format(business.price) }}
                            {% else %}
                                Price on Request
                            {% endif %}
                        </div>
                        
                        <div class="business-tags">
                            <span class="tag labor-{{ business.labor_intensity }}">
                                {{ business.labor_intensity }} labor
                            </span>
                            <span class="tag ai-risk">
                                {% if "low" in business.ai_disruptability.lower() %}
                                    Low AI Risk
                                {% elif "high" in business.ai_disruptability.lower() %}
                                    High AI Risk
                                {% else %}
                                    Medium AI Risk
                                {% endif %}
                            </span>
                        </div>
                        
                        <div class="business-details">
                            <div class="detail-item">
                                <div class="detail-label">Location</div>
                                <div class="detail-value">{{ business.address }}</div>
                            </div>
                            
                            <div class="detail-item">
                                <div class="detail-label">Distance</div>
                                <div class="detail-value">
                                    {% if business.distance_miles %}
                                        {{ business.distance_miles }} miles
                                    {% else %}
                                        Calculating...
                                    {% endif %}
                                </div>
                            </div>
                            
                            <div class="detail-item">
                                <div class="detail-label">Visit Frequency</div>
                                <div class="detail-value">{{ business.visit_frequency|title }}</div>
                            </div>
                            
                            <div class="detail-item">
                                <div class="detail-label">Sale Reason</div>
                                <div class="detail-value">{{ business.reason_for_sale|title }}</div>
                            </div>
                            
                            {% if business.earnings_multiple > 0 %}
                            <div class="detail-item">
                                <div class="detail-label">Earnings Multiple</div>
                                <div class="detail-value">{{ business.earnings_multiple }}x</div>
                            </div>
                            {% endif %}
                            
                            {% if business.ownership_structure != "unknown" %}
                            <div class="detail-item">
                                <div class="detail-label">Ownership</div>
                                <div class="detail-value">{{ business.ownership_structure }}</div>
                            </div>
                            {% endif %}
                        </div>
                        
                        {% if business.ai_disruptability %}
                        <div class="ai-assessment">
                            <strong>AI Assessment:</strong> {{ business.ai_disruptability }}
                        </div>
                        {% endif %}
                        
                        {% if business.partial_match_explanation %}
                        <div class="ai-assessment" style="border-left-color: #f39c12;">
                            <strong>Note:</strong> {{ business.partial_match_explanation }}
                        </div>
                        {% endif %}
                        
                        <a href="{{ business.listing_url }}" target="_blank" class="business-link">
                            View Full Listing →
                        </a>
                    </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="no-results">
                    <h3>No Qualifying Businesses Found</h3>
                    {% if data.no_matches_reason %}
                        <p>{{ data.no_matches_reason }}</p>
                    {% endif %}
                    <p>Try adjusting the search criteria or check back tomorrow for new listings.</p>
                </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Dashboard generated on {{ generated_time }} | Data from {{ scan_date[:10] if scan_date else 'Unknown Date' }}</p>
            <p>Tracking {{ data.summary.platform_counts|length }} platforms for business opportunities</p>
        </div>
    </div>
</body>
</html>
        """
        return Template(template_str)

def generate_latest_dashboard():
    """Generate dashboard from the most recent JSON file"""
    import glob
    
    # Find the most recent JSON file
    json_files = glob.glob("business_listings_*.json")
    if not json_files:
        print("No business listing JSON files found.")
        return
    
    latest_file = max(json_files, key=os.path.getctime)
    print(f"Generating dashboard from: {latest_file}")
    
    generator = DashboardGenerator()
    output_file = generator.generate_dashboard(latest_file)
    
    print(f"Dashboard generated: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_latest_dashboard()
